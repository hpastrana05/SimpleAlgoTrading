import time
import pandas_ta as ta

from trading_api import *
from classes.data_manager import DataManager



def main():
    print("Algo Trading script running...")
    # Ticker for the T212 api
    ticker = "AAPL_US_EQ"

    can_trade = False

    # Gets all the available instruments on the moment
    avail = get_available_instruments()
    avail_list = []
    if avail:
        for data in avail:
            avail_list.append((data["ticker"], data["currencyCode"]))

        for pair in avail_list:
            if pair[0] == ticker:
                can_trade = True

    # Indicators needed for the Strategy
    indicators = {
        "EMA": [10, 25]
    }

    # Data manager
    dm = DataManager("AAPL", indicators, "1m", "1D")

    # Timers for the API calls
    current_time = time.time()
    running_check_timer = current_time
    avail_list_timer = current_time
    data_timer = current_time

    last_quantity = 0
    position_open = False

    while True:
        current_time = time.time()

        acc_data = get_account_summary()
        usable_money = acc_data['cash']['availableToTrade']

        # Every 30 minutes prints the state of the bot
        if current_time - running_check_timer >= 60*30:
            running_check_timer = current_time
            print("Running check:")
            run = f"\tActual usable money: {usable_money}\n" \
                  f"\tCurrent time: {current_time}\n" \
                  f"\tPosition open: {position_open}\n"\
                  f"\tLast data update: {data_timer}\n"\
                  f"\tLast available list update: {avail_list_timer}\n"
            print(run)


        #Fetch actual data
        if current_time - data_timer >= 60:
            # print("Data Updated")
            dm.update_data()
            data_timer = current_time

        # Fetch available items
        if current_time - avail_list_timer >= 60:
            avail = get_available_instruments()
            avail_list_timer = time.time()

            # If no response it doesn't update it
            if avail:
                # print("Available List updated")
                avail_list = []
                for data in avail:
                    avail_list.append((data["ticker"], data["currencyCode"]))

                can_trade = False
                for pair in avail_list:
                    if pair[0] == ticker:
                        can_trade = True

                    if can_trade:
                        break

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

        time.sleep(5)



if __name__ == "__main__":
    main()