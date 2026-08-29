import yfinance as yf
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)  # blocks non-critical errors like 404 when user inputs invalid ticker

def get_stock():
    stock_info = []
    while True:   # verify if user input is a real stock name / ticker
        query = input("Enter a ticker symbol or a stock name\n").upper()
        try:
            search_results = yf.Search(query, max_results = 5).quotes
            if search_results == []:
                print(f"No matching results for '{query}'Make sure you check the spelling!\n")
            else:
                for i, result in enumerate(search_results):
                    shortname = result.get("shortname", "N/A") # takes 'unknown' if the key doesnt have a pair
                    symbol = result.get("symbol", "N/A")
                    exchange = result.get("exchange", "N/A")
                    print(f"{i+1}. {symbol}: {shortname}: {exchange}")
                stock_choice = input("Enter your choice 1-5 or press [ANY OTHER KEY] to search again\n")
                len_stk = len(search_results)
                if stock_choice.isdigit():
                    stock_cho = int(stock_choice)
                    if stock_cho <= len_stk and stock_cho>0:
                        stock_val = int(stock_choice)-1
                        stock_tic = search_results[stock_val].get("symbol","unknown")
                        stock_ticker = yf.Ticker(stock_tic)
                        stock_info.append(stock_ticker.info.get("allTimeHigh", 0)) # not brackets as it will crash if not find so use .get so if not found it can assign 0
                        current_price = round((stock_ticker.history(period = "1d")["Close"].iloc[-1]),2)
                        stock_info.append(current_price)
                        symbol_choice = search_results[stock_val].get("symbol","N/A")
                        stock_info.append(stock_ticker.info.get("displayName",symbol_choice))
                        return(stock_info)
                    elif stock_cho > len_stk or stock_cho<=0 :
                        word = f"You only have 1 option to chose from you cant chose {stock_cho}" if len_stk ==1 else f"You must pick a number between 1-{len_stk}!"
                        print(f"{word}")
                else:
                    print("If you cant find your stock make sre your spelling is correct and adjust for any capitals")
        except Exception as e:
            print(f"Sorry the market didnt behaves expected please try again soon\n{e}")
            

def get_details(max_price):   # get the amount invested and the price of the stock at the price invested into a list as a tuple
    x = 0
    purchases = []
    while x ==0:
        try:
            amount_invested = float(input("Enter amount of money invested at specific price in £\n"))
            if amount_invested >0:
                while True:
                    try:
                        share_price = float(input("Enter the price of the stock when you baught it in £\n"))
                        if share_price >0 and (max_price == 0 or share_price<=max_price):
                            purchases.append((amount_invested,share_price))
                            choice = input("Enter [E] to add another buy or [ANY OTHER KEY] to continue\n").lower()
                            if choice == "e":
                                break
                            else:
                                x+=1
                                return purchases
                        elif share_price<0:
                            print("Enter a share price more than 0")
                        elif share_price>max_price:
                            print(f"The max price was £{max_price} so you couldn't have baught it at £{share_price:.2f}!")
                    except:
                        print("Enter a valid number")
            else:
                print("The amount invested much be greater than £0.00")
        except:
            print("Make sure you enter a number!")

def price_average(purchases):  # calculates the average price amongst all of the amount and prices user has baught of the specific stock
    total_amount = 0
    total_shares = 0
    for amount, price in purchases:
        total_amount += amount
        total_shares += amount / price
    return[round((total_amount/total_shares) ,2),total_amount,total_shares]

def percent_change(average_price, current_price, display_name,total_shares): # calculates percentage change based on live data
    stock_worth = total_shares*current_price
    percent = (current_price-average_price)/average_price
    word = "up +" if percent > 0 else("down " if percent < 0 else "still at ")
    print(f"Your {word}{percent:.2%} so your total shares in {display_name} is worth around £{stock_worth:.2f}")





stock_info = get_stock()
max_price = stock_info[0]  # assigns variables to their list index that got returned in stock_info function
current_price = stock_info[1]
display_name = stock_info[2]  #
purchases = get_details(max_price)
avg_price_data = price_average(purchases)
average_price = avg_price_data[0]
total_amount = avg_price_data[1]
total_shares = avg_price_data[2]
percent_change(average_price, current_price, display_name,total_shares)