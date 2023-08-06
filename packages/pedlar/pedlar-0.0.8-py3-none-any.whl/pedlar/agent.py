"""mt5 zmq test client."""
import argparse
from collections import namedtuple
from datetime import datetime
import logging
import re
import struct

import requests
import zmq

from .utils import calc_profit

logger = logging.getLogger(__name__)
logger.info("libzmq: %s", zmq.zmq_version())
logger.info("pyzmq: %s", zmq.pyzmq_version())

# pylint: disable=broad-except,too-many-instance-attributes,too-many-arguments

Order = namedtuple('Order', ['id', 'price', 'volume', 'type'])

# Context are thread safe already,
# we'll create one global one for all agents
context = zmq.Context()


class Agent:
  """Base class for Pedlar trading agent."""
  name = "agent"
  polltimeout = 2000 # milliseconds
  csrf_re = re.compile('name="csrf_token" type="hidden" value="(.+)"')
  time_format = "%Y.%m.%d %H:%M:%S" # datetime column format

  def __init__(self, backtest=None, username="nobody", password="",
               ticker="tcp://localhost:7000",
               endpoint="http://localhost:5000"):
    self.backtest = backtest # backtesting file in any
    self._last_tick = (None, None) # last tick price for backtesting
    self._last_order_id = 0 # auto increment id for backtesting
    self.username = username # pedlarweb username
    self.password = password # pedlarweb password
    self.endpoint = endpoint # pedlarweb endpoint
    self._session = None # pedlarweb requests Session
    self.ticker = ticker # Ticker url
    self._poller = None # Ticker socket polling object
    self.orders = dict() # Orders indexed using order id
    self.balance = 0.0 # Local session balance

  @classmethod
  def from_args(cls, parents: list = None):
    """Create agent instance from command line arguments."""
    parser = argparse.ArgumentParser(description="Pedlar trading agent.",
                                     fromfile_prefix_chars='@',
                                     parents=parents or list())
    parser.add_argument("-b", "--backtest", help="Backtest agaisnt given file.")
    parser.add_argument("-u", "--username", default="nobody", help="Pedlar Web username.")
    parser.add_argument("-p", "--password", default="", help="Pedlar Web password.")
    parser.add_argument("-t", "--ticker", default="tcp://localhost:7000", help="Ticker endpoint.")
    parser.add_argument("-e", "--endpoint", default="http://localhost:5000", help="Pedlar Web endpoint.")
    return cls(**vars(parser.parse_args()))

  def connect(self):
    """Attempt to connect pedlarweb and ticker endpoints."""
    #-- pedlarweb connection
    # We will adapt to the existing web login rather than
    # creating a new api endpoint for agent requests
    logger.info("Attempting to login to Pedlar web.")
    _session = requests.Session()
    try:
      r = _session.get(self.endpoint+"/login") # CSRF protected
      r.raise_for_status()
    except:
      logger.critical("Failed to connect to Pedlar web.")
      raise RuntimeError("Connection to Pedlar web failed.")
    try:
      csrf_token = self.csrf_re.search(r.text).group(1)
    except AttributeError:
      raise Exception("Could not find CSRF token in auth.")
    payload = {'username': self.username, 'password': self.password,
               'csrf_token': csrf_token}
    r = _session.post(self.endpoint+"/login", data=payload, allow_redirects=False)
    r.raise_for_status()
    if not r.is_redirect or not r.headers['Location'].endswith('/'):
      raise Exception("Failed login into Pedlar web.")
    self._session = _session
    logger.info("Pedlar web authentication successful.")
    #-- ticker connection
    socket = context.socket(zmq.SUB)
    # Set topic filter, this is a binary prefix
    # to check for each incoming message
    # set from server as uchar topic = X
    # We'll subsribe to everything for now
    socket.setsockopt(zmq.SUBSCRIBE, bytes())
    # socket.setsockopt(zmq.SUBSCRIBE, bytes.fromhex('00'))
    logger.info("Connecting to ticker: %s", self.ticker)
    socket.connect(self.ticker)
    self._poller = zmq.Poller()
    self._poller.register(socket, zmq.POLLIN)

  def disconnect(self):
    """Close server connection gracefully in any."""
    # Clean up remaining orders
    self.close()
    # Ease the burden on server and logout
    logger.info("Logging out of Pedlar web.")
    r = self._session.get(self.endpoint+"/logout", allow_redirects=False)
    if not r.is_redirect:
      logger.warning("Could not logout from Pedlar web.")

  def on_order(self, order: Order):
    """Called on successful order."""
    pass

  def talk(self, order_id: int = 0, volume: float = 0.01, action: int = 0):
    """Make a request response attempt to Pedlar web."""
    payload = {'order_id': order_id, 'volume': volume, 'action': action,
               'name': self.name}
    try:
      r = self._session.post(self.endpoint+'/trade', json=payload)
      r.raise_for_status()
      resp = r.json()
    except Exception as e:
      logger.error("Pedlar web communication error: %s", str(e))
      raise IOError("Pedlar web server communication error.")
    return resp

  def _place_order(self, otype: str = "buy", volume: float = 0.01, single: bool = True, reverse: bool = True):
    """Place a buy or a sell order."""
    ootype = "sell" if otype == "buy" else "buy" # Opposite order type
    if (reverse and
        not self.close([oid for oid, o in self.orders.items() if o.type == ootype])):
      # Attempt to close all opposite orders first
      return
    if single and [1 for o in self.orders.values() if o.type == otype]:
      # There is already an order of the same type
      return
    # Request the actual order
    logger.info("Placing a %s order.", otype)
    try:
      if self.backtest:
        # Check last tick exists:
        if self._last_tick[0] is None or self._last_tick[1] is None:
          raise ValueError(f"No last tick data: {self._last_tick}")
        # Place order locally
        bidaskidx = 0 if otype == "buy" else 1
        order = Order(id=self._last_order_id+1, price=self._last_tick[bidaskidx],
                      volume=volume, type=otype)
      else:
        # Contact pedlarweb
        resp = self.talk(volume=volume, action=2 if otype == "buy" else 3)
        order = Order(id=resp['order_id'], price=resp['price'], volume=volume, type=otype)
      self._last_order_id = order.id
      self.orders[order.id] = order
      self.on_order(order)
    except Exception as e:
      logger.error("Failed to place %s order: %s", otype, str(e))

  def buy(self, volume: float = 0.01, single: bool = True, reverse: bool = True):
    """Place a new buy order and store it in self.orders
    :param volume: size of trade
    :param single: only place if there is not an already
    :param reverse: close sell orders if any
    """
    self._place_order(otype="buy", volume=volume, single=single, reverse=reverse)

  def sell(self, volume: float = 0.01, single: bool = True, reverse: bool = True):
    """Place a new sell order and store it in self.orders
    :param volume: size of trade
    :param single: only place if there is not an already
    :param reverse: close buy orders if any
    """
    self._place_order(otype="sell", volume=volume, single=single, reverse=reverse)

  def on_order_close(self, order: Order, profit: float):
    """Called on successfull order close."""
    pass

  def close(self, order_ids: list = None):
    """Close open all orders or given ids
    :param order_ids: only close these orders
    :return: true on success false otherwise
    """
    oids = order_ids if order_ids is not None else list(self.orders.keys())
    for oid in oids:
      if self.backtest:
        # Execute order locally
        order = self.orders.pop(oid)
        _, profit = calc_profit(order, *self._last_tick)
        logger.info("Closed order %s with profit %s", oid, profit)
        self.balance += profit
        self.on_order_close(order, profit)
      else:
        # Contact pedlarweb
        try:
          resp = self.talk(order_id=oid, action=1)
          order = self.orders.pop(oid)
          logger.info("Closed order %s with profit %s", oid, resp['profit'])
          self.balance += resp['profit']
          self.on_order_close(order, resp['profit'])
        except Exception as e:
          logger.error("Failed to close order %s: %s", oid, str(e))
          return False
    return True

  def on_tick(self, bid: float , ask: float, time: datetime = None):
    """Called on every tick update.
    :param bid: latest bid price
    :param ask: latest asking price
    :param time: datetime of tick
    """
    pass

  def on_bar(self, bopen: float, bhigh: float, blow: float, bclose: float, time: datetime = None):
    """Called on every last bar update.
    :param bopen: opening price
    :param bhigh: highest price
    :param blow: lowest price
    :param bclose: closing price
    :param time: datetime of bar
    """
    pass

  def remote_run(self):
    """Start main loop and receive updates."""
    # Check connection
    if not self._session:
      self.connect()
    # We'll trade forever until interrupted
    logger.info("Starting main trading loop...")
    try:
      while True:
        socks = self._poller.poll(self.polltimeout)
        if not socks:
          continue
        raw = socks[0][0].recv()
        # unpack bytes https://docs.python.org/3/library/struct.html
        if len(raw) == 17:
          # We have tick data
          bid, ask = struct.unpack_from('dd', raw, 1) # offset topic
          self.on_tick(bid, ask, datetime.now())
        elif len(raw) == 33:
          # We have bar data
          bo, bh, bl, bc = struct.unpack_from('dddd', raw, 1) # offset topic
          self.on_bar(bo, bh, bl, bc, datetime.now())
    finally:
      logger.info("Stopping agent...")
      self.disconnect()

  def local_run(self):
    """Run agaisnt local backtesting file."""
    import csv
    with open(self.backtest, newline='', encoding='utf-16') as csvfile:
      reader = csv.reader(csvfile)
      try:
        for row in reader:
          if row[0] == 'tick':
            # Check if time column exists
            time = datetime.strptime(row.pop(), self.time_format) if len(row) > 3 else None
            self._last_tick = tuple([float(x) for x in row[1:]])
            self.on_tick(*self._last_tick, time=time)
          elif row[0] == 'bar':
            # Check if time column exists
            time = datetime.strptime(row.pop(), self.time_format) if len(row) > 5 else None
            self.on_bar(*[float(x) for x in row[1:]], time=time)
      except KeyboardInterrupt:
        pass # Nothing to do
      finally:
        print("--------------")
        print("Final session balance:", self.balance)
        print("--------------")

  def run(self):
    """Run agent."""
    if self.backtest:
      self.local_run()
    else:
      self.remote_run()
