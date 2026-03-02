import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from trading_api import get_available_instruments, get_account_summary
from classes.strategy_manager import StrategyManager

class TradingEngine:

    def __init__(self, strategy_list):
        self.account_summary = {}
        self.usable_money = 0
        self.current_tickers = []
        self.acc_value = 0 
        self.investments_value = 0
        self.strategies = None

        self.update_summary_values()
        self.update_current_tickers()
        self.insert_strategies(strategy_list)

    def fetch_tradable_tickers(self) -> list[str]:
        """
        This method returns a list with all current available tickers
        return: list[tickers] or None if error
        1req / 50s
        """
        avail = get_available_instruments()
        # print(avail)
        avail_list = []
        if avail:
            for data in avail:
                avail_list.append(data["ticker"])
            return avail_list
        return None
    
    def ticker_availability(self, ticker:str) -> bool:
        """
        Returns if the ticker is currently available
        return: bool
        """
        avail_list = self.current_tickers
        #print(avail_list)
        return ticker in avail_list

    def update_current_tickers(self):
        """
        Updates the list of current tickers
        1req / 50s
        """
        avail = self.fetch_tradable_tickers()
        if avail:
            self.current_tickers = avail
        

    def fetch_acc_summary(self) -> dict:
        """
        Returns actual account summary
        return: dict
        1req / 5s
        """
        acc_sum = get_account_summary()
        return acc_sum
    
    def _update_acc_summary(self):
        """Fetches the new acc summary and if it works it updated the data"""
        summ = self.fetch_acc_summary()
        if summ:
            self.account_summary = summ
    
    def _update_usable_money(self):
        """
        Retrieves the cash amount from account summary
        """
        if self.account_summary:
            self.usable_money = self.account_summary['cash']['availableToTrade']
    
    def _update_strategy_money(self):
        """
        TODO: Updates the money for the strategies
        """
        pass

    def _update_acc_value(self):
        """
        Retrieves the total account value from summary
        """
        if self.account_summary:
            self.acc_value = self.account_summary["totalValue"]
    
    def _update_investments_value(self):
        """
        Retrieves investments value from summary
        """
        if self.account_summary:
            self.investments_value = self.account_summary["investments"]["currentValue"]

    def update_summary_values(self):
        """
        Updates all values from account summary
        1req / 5s
        """
        self._update_acc_summary()
        self._update_usable_money()
        self._update_investments_value()
        self._update_acc_value()

    def show_running_status(self):
        """
        Print the actual status of the program
        """

        print("Running check:")
        run = f"\tActual usable money: {self.usable_money}\n" \
              f"\tActual account value: {self.acc_value}\n" \
              
        print(run)

    def insert_strategies(self, strategy_list):
        """
        Initializes the strategies on the list
        TODO: Add weights/money to strategies for the money they will operate
        """
        final_list = []
        for strategy in strategy_list:
            strat = StrategyManager(**strategy)
            final_list.append(strat)
        
        self.strategies = final_list

    def check_strategies(self):
        """
        Should be runned with acc summary values updated
        TODO: give the money to the strategies 
        """
        for strat in self.strategies:
            # Right now uses all the money (1 strategy)
            strat.check_strategy(self.usable_money)
    
    def update_data(self):
        """
        Updates data manager on all stratgies
        """
        for strat in self.strategies:
            strat.update_data()