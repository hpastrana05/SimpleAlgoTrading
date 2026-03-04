import yfinance as yf
import time
from datetime import datetime

ticker = "AAPL"
interval = "1m"
period = "1D"

while True:
    now = datetime.now()

    if now.second == 0:
        df = yf.download(ticker, interval=interval, period=period, )

        print(df.tail(2))

    time.sleep(1)