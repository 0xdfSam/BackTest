from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
import config

class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

class IBClient:
    def __init__(self):
        self.app = IBApi()
        self.connected = False

    def connect(self):
        if not self.connected:
            self.app.connect(config.IB_HOST, config.IB_PORT, config.IB_CLIENT_ID)
            self.app.run()
            self.connected = True

    def disconnect(self):
        if self.connected:
            self.app.disconnect()
            self.connected = False

    def get_contract(self, symbol):
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        return contract

    def place_order(self, contract: Contract, order: dict):
        """
        Places an order for the given contract with specified parameters.
        
        :param contract: The contract object representing the security to be traded.
        :param order: A dictionary containing order details (e.g., {'action': 'BUY', 'quantity': 100, 'orderType': 'MARKET'})
        """
        order_id = self.app.nextOrderId()
        action = order['action']
        quantity = order['quantity']
        order_type = order['orderType']
        
        if order_type == 'LIMIT':
            limit_price = order.get('limitPrice', None)
            self.app.placeOrder(order_id, contract, action, quantity, order_type, price=limit_price)
        else:
            self.app.placeOrder(order_id, contract, action, quantity, order_type)

    def request_market_data(self, contract: Contract):
        """
        Requests market data for the given contract.
        
        :param contract: The contract object representing the security to be traded.
        """
        self.app.reqMktData(self.app.nextOrderId(), contract, '', False)

    def cancel_order(self, order_id):
        """
        Cancels an order with the specified order ID.
        
        :param order_id: The unique identifier of the order to be canceled.
        """
        self.app.cancelOrder(order_id)

    def req_historical_data(self, contract: Contract, duration: str, bar_size: str, what_to_show: str):
        """
        Requests historical data for the given contract with specified parameters.
        
        :param contract: The contract object representing the security to be traded.
        :param duration: The length of time covered by the request (e.g., '30 D' for 30 days).
        :param bar_size: The size of each bar in the historical data (e.g., '1 day', '1 hour').
        :param what_to_show: The type of data to be shown ('TRADES', 'MIDPOINT', etc.).
        """
        self.app.reqHistoricalData(self.app.nextOrderId(), contract, '', duration, bar_size, what_to_show, 0, 2, False, [])

