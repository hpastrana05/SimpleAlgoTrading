import time
import pandas_ta as ta
from datetime import datetime

from trading_api import *
from classes.data_manager import DataManager
from classes.trading_engine import TradingEngine



def main():
    print("Algo Trading script running...")
    # Ticker for the T212 api

    # CONFIG
    ticker_data = "AAPL"
    ticker_api = "AAPL_US_EQ" 
    interval = "1m"
    period = "1D"
    # Indicators needed for the Strategy
    indicators = {
        "EMA": [10, 25]
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

    te = TradingEngine(strategy_list)


    can_trade = False

    # Gets all the available instruments on the moment
    # Job for the trading Organizer -> get_tickers()
    can_trade = te.ticker_availability(ticker_api)


    # Timers for the API calls
    current_time = time.time()
    acc_summary_timer = current_time
    running_check_timer = current_time - 60*30
    avail_list_timer = current_time
    data_timer = current_time

    data_updated = False
    last_quantity = 0
    position_open = False

    while True:
        current_time = time.time()
        now = datetime.now()

        # Every 5 seconds updates acc summary
        if current_time - acc_summary_timer >= 5:
            te.update_summary_values()

        # Every 50 seconds updates tradable tickers
        if current_time - avail_list_timer >= 50:
            te.update_current_tickers()
            can_trade = te.ticker_availability(ticker_api)

        # Every 30 minutes prints the state of the bot
        if current_time - running_check_timer >= 60*30:
            # Job fof Trading Organizer -> print_status()
            running_check_timer = current_time

            current_date = datetime.fromtimestamp(current_time).strftime("%d/%m/%Y %H:%M:%S")
            data_update_date = datetime.fromtimestamp(data_timer).strftime("%d/%m/%Y %H:%M:%S")
            avail_list_date = datetime.fromtimestamp(avail_list_timer).strftime("%d/%m/%Y %H:%M:%S")

            print(f"Running check at: {current_date}")
            run = f"\tActual usable money: {te.usable_money}\n" \
                  f"\tPosition open: {position_open}\n"\
                  f"\tLast data update: {data_update_date}\n"\
                  f"\tLast available list update: {avail_list_date}\n"
            print(run)


        #Fetch actual data -> cambiar a cuando los segundos sean 0
        if now.second == 0:
            if not data_updated:
                te.update_data()
                data_updated = True
                data_timer = current_time

        else: data_updated = False

        if not can_trade:
            time.sleep(60)
            continue

        # Check the strategies in the TradingEngine
        te.check_strategies()

        time.sleep(0.01)


if __name__ == "__main__":
    main()