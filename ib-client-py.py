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

    # Add methods for placing orders, requesting data, etc.
