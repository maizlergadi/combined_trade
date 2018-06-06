from bitex.api.WSS.bitstamp import BitstampWSS
from bitfinex_orderbook import BitfinexOrderbook
from queue import PriorityQueue
import heapq
import operator

class UnifiedOrderbook:
    def __init__(self, orderbooks):
        self._orderbooks = orderbooks
        self._is_thread_orderbook = False

    def set_orderbook(self, exchange, orderbook):
        if exchange in self._orderbooks:
            self._orderbooks[exchange] = orderbook

    def get_unified_orderbook(self, symbol, size):
        client_orderbooks = []
        for curr_orderbook in self._orderbooks:
            client_orderbooks.append(self._orderbooks[curr_orderbook].get_current_partial_book(symbol, size))
        best_orders = {'asks' : [], 'bids' : []}
        order_keys = [[heapq.nsmallest, 'asks'], [heapq.nlargest, 'bids']]
        for curr_orderbook in client_orderbooks:
            for curr_keyset in order_keys:
                best_orders[curr_keyset[1]] = curr_keyset[0](size, best_orders[curr_keyset[1]] + curr_orderbook[curr_keyset[1]], key=operator.itemgetter('price'))

        return best_orders

    def is_thread_orderbook(self):
        return False

    def get_current_spread_and_price(self, asset_pair):
        best_orders = self.get_unified_orderbook(asset_pair, 1)
        spread_and_price = {'ask': 0, 'bid': 0}
        if len(best_orders['asks']) > 0:
            spread_and_price['ask'] = best_orders['asks'][0]['price']
        if len(best_orders['bids']) > 0:
            spread_and_price['bid'] = best_orders['bids'][0]['price']
        return spread_and_price

    def get_average_spread(self, asset_pair):
        return 0
