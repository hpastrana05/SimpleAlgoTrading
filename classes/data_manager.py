import yfinance as yf
import datetime as dt
import pandas as pd
import pandas_ta as ta

class DataManager:
    def __init__(self, ticker, indicators, interval, period=None):
        self.ticker = ticker
        self.indicators = indicators
        self.interval = interval
        self.period = period
        self.now = dt.datetime.now()
        self.data = self.fetch_data(ticker, interval, period)
        self.add_indicators(indicators)


    def fetch_data(self, ticker, interval, period):
        data = yf.download(ticker, interval=interval, period=period, progress=False)
        # Only one entry not two
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.droplevel(1)
        return pd.DataFrame(data)

    def update_data(self):
        """Will update the data and remove old data rows to maintain a fixed window size."""
        data_len = len(self.data)
        new_data = self.fetch_data(self.ticker, self.interval, self.period)
        self.data = pd.concat([self.data, new_data]).drop_duplicates().reset_index(drop=True)
        while len(self.data) > data_len:
            self.data = self.data[1:]
    
    def add_indicators(self, indicators):
        """Add technical indicators to the data."""
        for name, values in indicators.items():
            for value in values:
                if name == "EMA":               
                    self.data[f"EMA_{value}"] = ta.ema(self.data["Close"], length=value)
                elif name == "RSI":
                    self.data[f"RSI_{value}"] = ta.rsi(self.data["Close"], length=value)
                elif name == "SMA":
                    self.data[f"SMA_{value}"] = ta.sma(self.data["Close"], length=value)
                elif name == "WMA":
                    self.data[f"WMA_{value}"] = ta.wma(self.data["Close"], length=value)
                elif name == "BBands":
                    bbands = ta.bbands(self.data["Close"], length=value[0], std=value[1])
                    self.data[f'BBands_{value}'] = bbands
                elif name == "EMA_CROSS":
                    self.data[f"EMA_CROSS_{value}"] = ta.cross(self.data[f"EMA_{value[0]}"], self.data[f"EMA_{value[1]}"])
'''
indicators = {
    "EMA": [10, 20],
    "RSI": [14],
    "SMA": [50],
    "WMA": [30],
    "BBands": [(20, 2)]
}
dm = DataManager("AAPL", indicators, "1m", "1D")

print(dm.data.columns)
print(dm.data.tail())

'''

