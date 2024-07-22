import sys
from ib_connection.ib_client import IBClient
from strategy.sample_strategy import SampleStrategy
from backtesting.backtest_engine import BacktestEngine

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [backtest|live]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "backtest":
        engine = BacktestEngine()
        strategy = SampleStrategy()
        engine.run(strategy)
    elif mode == "live":
        ib_client = IBClient()
        ib_client.connect()
        strategy = SampleStrategy()
        strategy.run(ib_client)
    else:
        print("Invalid mode. Use 'backtest' or 'live'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
