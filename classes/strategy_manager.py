import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas_ta as ta
from datetime import datetime

from classes.data_manager import DataManager
from classes.signal_classes import *
from trading_api import post_place_market_order


class StrategyManager:

    def __init__(self, name: str, ticker_api:str, ticker_data:str, indicators:dict, interval:str, period:str, entry_rule:dict, exit_rule:dict):
        self.name = name
        self.ticker = ticker_api
        self.indicators = indicators
        self.dm = DataManager(ticker_data, indicators, interval, period)

        self.entry_signal = build_signal(entry_rule)
        self.exit_signal = build_signal(exit_rule)

        self.position_open = False
        self.position_quantity = 0


    def check_entry(self):
        """Checks entry function"""
        return self.entry_signal.evaluate(self.dm.data) 


    def check_exit(self):
        """
        Right now simple EMA cross 10 25
        """
        return self.exit_signal.evaluate(self.dm.data)
    
    def buy_position(self, money):
        """
        Buys in the position
        """
        quantity = money*0.95/self.dm.data["Close"].iloc[-1]
        quantity = round(quantity, 4)
        response = post_place_market_order(quantity, self.ticker)
        if response:
            self.position_open = True
            self.position_quantity = quantity
            print(f"Market order BUY placed at: {response["createdAt"]}\n Ticker: {response['ticker']} \n Quantity: {response['quantity']}")
        else:
            print("Error on BUY order")

    def sell_position(self):
        """
        Sells in the position
        """
        response = post_place_market_order(-self.position_quantity, self.ticker)
        if response:
            print(f"Market order SELL placed at: {response["createdAt"]}\n Ticker: {response['ticker']} \n Quantity: {response['quantity']}")
            self.position_open = False
            self.position_quantity = 0
        else:
            print("Error on SELL order")
    
    def check_strategy(self, money):
        """
        Checks parts of the strategy.
        """
        now = datetime.now()

        if self.check_entry() and not self.position_open and not (now.hour == 21 and now.minute >= 58) :
            self.buy_position(money)

        if self.position_open and self.check_exit():
            self.sell_position()
        
        if now.hour == 21 and now.minute == 58:
            self.sell_position()


    def update_data(self):
        self.dm.update_data()
    
    def check_last_entries(self):
        cross_sequence = list(ta.cross(self.dm.data["EMA_10"], self.dm.data["EMA_25"], above=True, equal=False))
        for cross in cross_sequence:
            if cross == 1:
                print("found")
        
        

"""
{
    "name": "Nombre",
    "ticker_api": "ticker",
    "ticker_data": "ticker"
    "indicators": {}
    "interval": "1m"
    "period": "1D"
    "entry_rule": {}, # plug directly the function
    "close_rule": {},
    
}
"""
"""
"entry_rule": {         //Also for close_rule
    "type": "AND",
    "signals": [
        {"type": "ema_cross_above", "fast": 10, "slow": 25},
        {"type": "rsi_oversold", "period": 14, "threshold": 30}
    ]
}
"""

"""
ticker_data = "AAPL"
ticker_api = "AAPL_US_EQ" 
interval = "1m"
period = "1D"
# Indicators needed for the Strategy
indicators = {
    "EMA": [10, 25]
}

strategy = {
        "name": "Strategia 1",
        "ticker_api": ticker_api,
        "ticker_data": ticker_data,
        "indicators": indicators,
        "interval": interval,
        "period": period,
    }


strat = StrategyManager(**strategy)

strat.check_last_entries()
"""