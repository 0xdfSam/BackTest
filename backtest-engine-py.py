import pandas as pd
import matplotlib.pyplot as plt
import config

class BacktestEngine:
    def __init__(self):
        self.initial_capital = config.INITIAL_CAPITAL
        self.start_date = config.START_DATE
        self.end_date = config.END_DATE

    def load_data(self):
        # Load historical data from CSV file
        data = pd.read_csv('data/historical_data.csv', index_col='Date', parse_dates=True)
        return data[(data.index >= self.start_date) & (data.index <= self.end_date)]

    def run(self, strategy):
        data = self.load_data()
        signals = strategy.backtest(data)
        
        # Calculate returns
        signals['Returns'] = np.log(signals['Close'] / signals['Close'].shift(1))
        signals['Strategy_Returns'] = signals['Position'].shift(1) * signals['Returns']
        
        # Calculate cumulative returns
        signals['Cumulative_Returns'] = (1 + signals['Returns']).cumprod()
        signals['Cumulative_Strategy_Returns'] = (1 + signals['Strategy_Returns']).cumprod()
        
        # Plot results
        plt.figure(figsize=(10, 6))
        plt.plot(signals.index, signals['Cumulative_Returns'], label='Buy and Hold')
        plt.plot(signals.index, signals['Cumulative_Strategy_Returns'], label='Strategy')
        plt.legend()
        plt.title('Backtest Results')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Returns')
        plt.show()

        # Print performance metrics
        total_return = signals['Cumulative_Strategy_Returns'].iloc[-1] - 1
        sharpe_ratio = np.sqrt(252) * signals['Strategy_Returns'].mean() / signals['Strategy_Returns'].std()
        
        print(f"Total Return: {total_return:.2%}")
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
