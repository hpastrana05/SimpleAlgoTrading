import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas_ta as ta

from classes.data_manager import DataManager
from trading_api import post_place_market_order

class StrategyManager:

    def __init__(self, name, ticker_api, ticker_data, indicators, temporality, period):
        self.name = name
        self.ticker = ticker_api
        self.indicators = indicators
        self.dm = DataManager(ticker_data, indicators, temporality, period)

        self.position_open = False
        self.position_quantity = 0


    def check_entry(self):
        """
        Right now simple EMA cross 10 25
        """
        entry_check = False
        cross_sequence = list(ta.cross(self.dm.data["EMA_10"], self.dm.data["EMA_25"], above=True, equal=False))
        if cross_sequence[-2] == 1 and not self.position_open:
            entry_check = True
        
        return entry_check

    def check_exit(self):
        """
        Right now simple EMA cross 10 25
        """
        exit_check = False
        if self.position_open:
            cross_sequence = list(ta.cross(self.dm.data["EMA_10"], self.dm.data["EMA_25"], above=False, equal=False))
            if cross_sequence[-2] == 1:
                exit_check = True

        return exit_check
    
    def buy_position(self, money):
        """
        Buys in the position
        """
        quantity = money*0.95/dm.data["Close"].iloc[-1]
        quantity = round(quantity, 4)
        response = post_place_market_order(quantity, self.ticker)
        if response:
            self.position_open = True
            self.position_quantity = quantity
            print(f"Market order BUY placed at: {response["createdAt"]}\n Ticker: {response['ticker']} \n Quantity: {response['quantity']}")

            print(f"Usable money: {usable_money*0.05}")
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
        if self.check_entry():
            self.buy_position(money)

        if self.check_exit():
            self.sell_position()


"""
{
    "name": "Nombre",
    "ticker": "ticker",
    "interval": "interval",
    "entry_rules": {},
    "close_rules": {},
    "indicators": {}
}
"""