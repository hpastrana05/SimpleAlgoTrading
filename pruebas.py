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
    temporality = "1m"
    # Indicators needed for the Strategy
    indicators = {
        "EMA": [10, 25]
    }

    # Data manager
    dm = DataManager(ticker_data, indicators, temporality, "1D")
    te = TradingEngine()


    can_trade = False

    # Gets all the available instruments on the moment
    # Job for the trading Organizer -> get_tickers()
    can_trade = te.ticker_availability(ticker_api)


    # Timers for the API calls
    current_time = time.time()
    acc_summary_timer = current_time
    running_check_timer = current_time
    avail_list_timer = current_time
    data_timer = current_time

    last_quantity = 0
    position_open = False

    while True:
        current_time = time.time()

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
        if current_time - data_timer >= 60:
            # print("Data Updated")
            dm.update_data()
            data_timer = current_time

        if not can_trade:
            time.sleep(60)
            continue


        """  Strategy ALL IN EMA CROSS   """
        # Entry position check
        entry_check = False
        cross_sequence = list(ta.cross(dm.data["EMA_10"], dm.data["EMA_25"], above=True, equal=False))
        if cross_sequence[-2] == 1 and not position_open:
            entry_check = True

        # Entry position
        if entry_check:
            quantity = usable_money*0.95/dm.data["Close"].iloc[-1]
            quantity = round(quantity, 4)
            response = post_place_market_order(quantity, ticker)
            if response:
                position_open = True
                last_quantity = quantity
                print(f"Market order BUY placed at: {response["createdAt"]}\n Ticker: {response['ticker']} \n Quantity: {response['quantity']}")

                print(f"Usable money: {usable_money*0.05}")
            else:
                print("Error on BUY order")
            # last_position_id = response['id']


        # Exit position check
        exit_check = False
        if position_open:
            cross_sequence = list(ta.cross(dm.data["EMA_10"], dm.data["EMA_25"], above=False, equal=False))
            if cross_sequence[-2] == 1:
                exit_check = True

        # Sell position check
        if exit_check:
            response = post_place_market_order(-last_quantity, ticker)
            if response:
                print(f"Market order SELL placed at: {response["createdAt"]}\n Ticker: {response['ticker']} \n Quantity: {response['quantity']}")
                position_open = False
                last_quantity = 0
            else:
                print("Error on SELL order")



if __name__ == "__main__":
    main()