import math
import yfinance as yf
import logging
logging.getLogger("yfinance").setLevel(logging.CRITICAL)  # blocks non-critical errors like 404 when user inputs invalid ticker
purchases =[]

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
                    shortname = result.get("shortname", "unknown") # gets 'unknown' if value of shortname isnt found
                    symbol = result.get("symbol", "unknown")
                    exchange = result.get("exchange", "unknown")
                    print(f"{i+1}. {symbol}: {shortname}: {exchange}")
                stock_choice = input("Enter your choice 1-5 or press [ANY OTHER KEY] to search again\n")
                if stock_choice in ["1","2","3","4","5"]:
                    stock_val = int(stock_choice)-1
                    stock_tic = search_results[stock_val].get("symbol","unknown")
                    stock_ticker = yf.Ticker(stock_tic)
                    stock_info.append(stock_ticker.info["allTimeHigh"])
                    stock_info.append(stock_ticker.info["regularMarketPrice"])
                    stock_info.append(stock_ticker.info["displayName"])
                    return(stock_info)
                else:
                    print("If you cant find your stock make sure your spelling is correct and adjust for any capitals")
        except Exception as e:
            print(f"Sorry the market didnt behaves expected please try again soon\n{e}")
            

def get_details(max_price):   # get the amount invested and the price of the stock at the price invested into a list as a tuple
    x = 0
    while x ==0:
        amount_invested = int(input("Enter amount of money invested at specific price £\n"))
        if amount_invested >0:
            while True:
                share_price = int(input("Enter the price of the stock when you baught it in £\n"))
                if share_price>0 and share_price <= max_price:
                    purchases.append((amount_invested,share_price))
                    continue_choice = input("Type [E] to add another buy or [OTHER KEY] if thats all\n").lower()
                    if continue_choice  == "e":
                        break
                    else:
                        x +=1
                        break
                elif share_price<0:
                    print("Enter a share price more than 0")
                elif share_price>max_price:
                    print(f"The max price was £{max_price} so you couldn't have baught it at £{share_price: .2f} it!")
        else:
            print("The amount invested much be greater than £0.00")

def price_average(purchases):
    total_amount = 0
    total_shares = 0
    for amount, price in purchases:
        total_amount += amount
        total_shares += amount / price
    average_price = math.floor((total_amount/total_shares)*100)/100
    return(average_price)

def percent_change(average_price,current_price,display_name):
    percent_change = (current_price/average_price)*100
    word = "up +" if percent_change > 0 else "down -"
    print(f"Your {word}{percent_change:.2f} on {display_name}")

stock_info = get_stock()
max_price = stock_info[0]
current_price = stock_info[1]
display_name = stock_info[2]
get_details(max_price)
average_price = price_average(purchases)
percent_change(average_price,current_price,display_name)