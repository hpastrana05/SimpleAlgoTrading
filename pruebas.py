import pandas_ta as ta
import time
from datetime import datetime
from trading_api import *
from classes.data_manager import DataManager
from classes.trading_engine import TradingEngine

ticker_data = "AAPL"
ticker_api = "AAPL_US_EQ" 
interval = "1m"
period = "1D"
# Indicators needed for the Strategy
indicators = {
    "EMA": [10, 25],
    "EMA_CROSS": [(10, 25)]
}


strategy_list = [
    {
        "name": "Strategia 1",
        "ticker_api": ticker_api,
        "ticker_data": ticker_data,
        "indicators": indicators,
        "interval": interval,
        "period": period,
    }
]

# te = TradingEngine(strategy_list)

dm = DataManager(ticker_data, indicators, interval, period)


"""

# Check data manager updates correctly
print("------DATA MANAGER---------")
print("tail:")
print(dm.data.tail())
print("head:")
print(dm.data.head())

for strat in te.strategies:   
    print("------strategy manager---------")
    print("tail:")
    print(strat.dm.data.tail())
    print("head:")
    print(strat.dm.data.head())


print(dm.data['EMA_CROSS_(10, 25)'])
found_list = []
for i, value in enumerate(dm.data['EMA_CROSS_(10, 25)']):
    if value == 1:
        found_list.append(i)
        print(f"Cross found in {i}")

for i in found_list:
    print("----------------------------------------------------------------------------")
    print(dm.data[['Close', "EMA_10", "EMA_25"]].iloc[i-1])
    print(dm.data[['Close', "EMA_10", "EMA_25"]].iloc[i])
    print(dm.data[['Close', "EMA_10", "EMA_25"]].iloc[i+1])
   

# Check the ta.cross works correctly
above_list = ta.cross(dm.data["EMA_10"], dm.data["EMA_25"], above=True, equal=False)
down_list = ta.cross(dm.data["EMA_10"], dm.data["EMA_25"], above=False, equal=False)

for i in range(len(above_list)):
    ab = above_list.iloc[i]
    dw = down_list.iloc[i]
    if ab == 1:
        print(f"Above cross found in {i}")
    if dw == 1:
        print(f"Down cross found in {i}")
""" 

# Checks the second 0 works
data_updated = False
while True:
    current_time = time.time()
    now = datetime.now()

    dm.update_data()
    print(".")
    time.sleep(0.01)