import yfinance as yf
import logging
import sqlite3

logging.getLogger("yfinance").setLevel(
    logging.CRITICAL)  # blocks non-critical errors like 404 when user inputs invalid ticker
currency_symbols = {
    "USD": "$",  # market currencies and they're symbols for better user readability
    "GBP": "£",
    "GBp": "p",
    "EUR": "€",
    "CAD": "CA$",
    "AUD": "A$",
    "JPY": "¥",
    "CHF": "CHF ",
    "CNY": "¥",
    "HKD": "HK$",
    "INR": "₹",
    "ZAR": "R",
    "SEK": "kr",
    "SGD": "S$",
    "BRL": "R$",
    "MXN": "Mex$",
    "NZD": "NZ$",
    "NOK": "kr",
    "DKK": "kr",
    "PLN": "zł",
    "KRW": "₩"}


class Database:
    def __init__(self, db_name="Portfolio.db"):
        self.db_name = db_name
        self.connection, self.cursor = self.db_sync()
    
    def db_sync(self):
        connection = sqlite3.connect(self.db_name)  # create the database and table
        cursor = connection.cursor()
        command1 = ("""CREATE TABLE IF NOT EXISTS portfolio(
                           buy_id INTEGER PRIMARY KEY,
                           symbol TEXT,
                           amount_invested FLOAT,
                           share_price FLOAT)""")
        cursor.execute(command1)
        connection.commit()
        return connection, cursor


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.ticker_obj = yf.Ticker(self.ticker)
    
    def get_current_price(self):
        current_data = self.ticker_obj.history(period="1d")
        if current_data.empty:
            return None
        return current_data["Close"].iloc[-1]
        
class Portfolio:
    def __init__(self,db_obj):
        self.db_obj = db_obj
    
    def get_grouped_stocks(self):
        query = """
                SELECT
                symbol,
                amount_invested,
                share_price
                FROM portfolio
                """
        grouped_stocks = self.db_obj.cursor.execute(query).fetchall()
        return (grouped_stocks)
    
    def price_average(self, grouped_stocks):
        names = []
        average_price = []
        for name, amount_invested, stock_price in grouped_stocks:
            if stock_price == 0:
                continue
            if name not in names:
                names.append(name)
                shares = amount_invested / stock_price
                average_p = amount_invested / shares
                average_price.append((average_p, name, shares, amount_invested))
            else:
                shares = amount_invested / stock_price
                for i, single_stock in enumerate(average_price):
                    if name in single_stock:
                        total_shares = single_stock[2] + shares
                        if amount_invested > 0:
                            total_amount = single_stock[3] + amount_invested
                            average_p = total_amount / total_shares if total_shares != 0 else 0
                        else:
                            average_p = single_stock[0]
                            total_amount = total_shares * average_p
                        average_price.pop(i)
                        average_price.append((average_p, name, total_shares, total_amount))
                        break
        return average_price

    def display_portfolio(self,average_price):  # calculates percentage change based on live data
        for stock in average_price:
            stock_ticker = yf.Ticker(stock[1])
            display_name = (stock_ticker.info.get("displayName", stock[1]))
            if stock[1] in currency_symbols:
                currency = currency_symbols[stock[1]]
            else:
                cur = stock_ticker.info.get("currency", "USD")
                currency = currency_symbols.get(cur, cur)  # cur, cur falls back on the currency if the symbol isnt found
            if stock[0] == 0 or stock[2] <= 0:
                print(f"You have sold all of your {display_name} shares the current holdings is {currency}0.00")
                continue
            else:
                price_history = stock_ticker.history(period = "1d")
                if price_history.empty:
                    print(f"Sorry we couldn't fetch the data for {display_name} right now\nPlease try again later")
                    continue
                current_price = round((stock_ticker.history(period="1d")["Close"].iloc[-1]), 2)
                percentage_change = round(((current_price - stock[0]) / stock[0]) * 100, 2)
                word = "up +" if (percentage_change / 100) > 0 else "down "
                print(
                    f"{display_name} is {word}{percentage_change}% your current holdings in {display_name} is {currency}{(current_price * stock[2]):.2f}")


def db_assign(symbol, cursor, connection, purchases):  # assign variables inputed into the database table
    for amount_invested, share_price in purchases:
        cursor.execute("INSERT INTO portfolio(symbol, amount_invested, share_price) VALUES(?,?,?)",
                       (symbol, amount_invested, share_price))
        connection.commit()


def get_stock(choice2, rows):
    stock_info = []
    while True:  # verify if user input is a real stock name / ticker
        print("If this was a mistake type [M] to go back to the menu")
        query = input("Enter a ticker symbol or a stock name\n").upper()
        if query.strip() == "M":
            return query
        try:
            search_results = yf.Search(query, max_results=5).quotes
            if search_results == []:
                print(f"No matching results for '{query}'Make sure you check the spelling!\n")
            else:
                for i, result in enumerate(search_results):
                    shortname = result.get("shortname", "N/A")  # takes 'unknown' if the key doesn't have a pair
                    symbol = result.get("symbol", "N/A")
                    exchange = result.get("exchange", "N/A")
                    print(f"{i + 1}. {symbol}: {shortname}: {exchange}")
                len_stk = len(search_results)
                stock_choice = input(f"Enter your choice 1-{len_stk} or press [ANY OTHER KEY] to search again\n")
                if stock_choice.isdigit():
                    stock_cho = int(stock_choice)
                    if stock_cho <= len_stk and stock_cho > 0:
                        stock_val = int(stock_choice) - 1
                        stock_tic = search_results[stock_val].get("symbol", "unknown")
                        if choice2 == "2":
                            owned_symbol = [row[0] for row in rows]
                            if stock_tic not in owned_symbol:
                                print(
                                    "You cannot sell something you dont even own!\nMake sure you declare your buys before you sell\n")
                                return False
                        stock_ticker = yf.Ticker(stock_tic)
                        stock_info.append(stock_ticker.info.get("allTimeHigh",0))  # not brackets as it will crash if not find so use .get so if not found it can assign 0
                        symbol_choice = search_results[stock_val].get("symbol", "N/A")
                        stock_info.append(stock_ticker.info.get("displayName", symbol_choice))
                        stock_info.append(stock_ticker.info.get("shortname", "N/A"))
                        stock_info.append(symbol_choice)
                        stock_currency = stock_ticker.info.get("currency","USD")  # gets currency symbol according to the market e.g. US market = $
                        currency = currency_symbols.get(stock_currency,
                                                        stock_currency)  # falls back on the stock_currency input if symbol isn't found inside our dictionary
                        stock_info.append(currency)
                        return (stock_info)
                    elif stock_cho > len_stk or stock_cho <= 0:
                        word = f"You only have 1 option to chose from you cant chose {stock_cho}" if len_stk == 1 else f"You must pick a number between 1-{len_stk}!"
                        print(f"{word}")
                else:
                    print("If you cant find your stock make sre your spelling is correct and adjust for any capitals")
        except Exception as e:
            print(f"Sorry the market didnt behaves expected please try again soon\nError:{e}")


def get_details(max_price, choice2, rows, symbol,
                currency):  # get the amount invested and the price of the stock at the price invested into a list as a tuple
    x = 0
    purchases = []
    while x == 0:
        try:
            word1 = "sold" if choice2 == "2" else "bought"
            print("If you have made a mistake type [M] to return to the main menu")
            amount_inv = input(f"Enter the amount you have {word1} of the stock, in {currency}\n").lower()
            if amount_inv.strip() == "m":
                x += 1
                return False
            amount_invested = float(amount_inv)
            if amount_invested > 0:
                while True:
                    print("If you have made a mistake type [M] to return to the main menu")
                    share_p = input(f"Enter the price of the stock when you {word1} it, in {currency}\n").lower()
                    if share_p.strip() == "m":
                        return False
                    try:
                        share_price = float(share_p)
                        if choice2 == "2":
                            total_shares = sum((row[1] / row[2]) for row in rows if symbol in row)
                            shares_2sell = amount_invested / share_price  # calculate the current value stock holdings not the amount deposited
                            total_value = total_shares * share_price
                            if shares_2sell > total_shares:
                                print(
                                    f"You couldn't have sold at {currency}{amount_invested:.2f} if you had {currency}{total_value:.2f} in {symbol} at {currency}{share_price}")
                                continue
                        if share_price > 0 and (max_price == 0 or share_price <= max_price):
                            purchases.append((amount_invested, share_price))
                            x += 1
                            return purchases
                        elif share_price < 0:
                            print("Enter a share price more than 0")
                        elif share_price > max_price:
                            print(
                                f"The max price was {currency}{max_price} so you couldn't have bought it at {currency}{share_price:.2f}!")
                    except ValueError:
                        print("Make sure you enter a valid number")
                        continue
            else:
                print(f"The amount invested much be greater than {currency}0.00")
        except ValueError:
            continue


def db_clear_symbol(symbol, cursor, connection):  # removes the row if we call to replace it
    cursor.execute("DELETE FROM portfolio WHERE symbol = ?", (symbol,))
    connection.commit()


def df_reset(cursor, connection):
    choice = input("Press [D] to confirm resetting your portfolio [ANY OTHER KEY] to return to the main menu\n").lower()
    if choice.strip() == "d":
        cursor.execute("DELETE FROM portfolio")
        connection.commit()
        print("Your table has been deleted")
    else:
        pass


choices_options = {"Declare a stock purchase to track on your portfolio": "1",
                   "Declare a stock sell to track on your portfolio": "2",
                   "Check my portfolio progress": "3",
                   "Declare the total amount you invested and the average price of your stock if available": "4",
                   "Reset your portfolio": "5"}
db = Database()
connection = db.connection
cursor = db.cursor
while True:
    print("\nEnter [ANY OTHER KEY] other than [1-5] if you want to stop the program")
    for chce, x in choices_options.items():
        print(f"{x}. {chce}")
    choice2 = input("Enter the number of the choice you would like!\n")
    match choice2:
        case "1":
            my_portfolio = Portfolio(db)
            rows = my_portfolio.get_grouped_stocks()
            stock_info = get_stock(choice2, rows)
            if stock_info == "M":
                continue
            else:
                max_price, display_name, shortname, symbol, currency = stock_info  # assigns variables to their list index that got returned in stock_info function
                purchases = get_details(max_price, choice2, rows, symbol, currency)
                if purchases == False:
                    pass
                else:
                    db_assign(symbol, cursor, connection, purchases)
                    my_portfolio = Portfolio(db)
                    rows = my_portfolio.get_grouped_stocks() # adds duplicate rows
                    connection.commit()
        case "2":
            my_portfolio = Portfolio(db)
            rows = my_portfolio.get_grouped_stocks()
            stock_info = get_stock(choice2, rows)
            if stock_info == "M" or stock_info == False:
                continue
            else:
                max_price, display_name, shortname, symbol, currency = stock_info
                purchases = get_details(max_price, choice2, rows, symbol, currency)
                if purchases == False:
                    pass
                else:
                    negative_sales = [(-amount, price) for amount, price in purchases]
                    db_assign(symbol, cursor, connection, negative_sales)
                    my_portfolio = Portfolio(db)
                    rows = my_portfolio.get_grouped_stocks()
                    connection.commit()
        
        case "3":
            my_portfolio = Portfolio(db)
            rows = my_portfolio.get_grouped_stocks()
            grouped_stocks = my_portfolio.get_grouped_stocks()
            if grouped_stocks == []:
                print("Sorry your portfolio is empty, nothing to show you!")
                continue
            else:
                average_price = my_portfolio.price_average(grouped_stocks)
                my_portfolio.display_portfolio(average_price)
                connection.commit()
        case "4":
            my_portfolio = Portfolio(db)
            rows = my_portfolio.get_grouped_stocks()
            stock_info = get_stock("1", rows)
            if stock_info == "M":
                continue
            else:
                try:
                    print("If you have made a mistake type [M] to return to the main menu")
                    total_am = input(f"Enter your total amount invested in {stock_info[1]} / net deposits\n").lower()
                    if total_am.strip() == "m":
                        continue
                    else:
                        total_amount = float(total_am)
                        print("If you have made a mistake type [M] to return to the main menu")
                        average_p = input(
                            f"Enter the average price you paid for {stock_info[1]} (can be found on your broker app)\n").lower()
                        if average_p.strip() == "m":
                            continue
                        else:
                            average_price = float(average_p)
                            symbol = stock_info[3]
                            stock_ticker = yf.Ticker(symbol)
                            max_price = stock_ticker.info.get("allTimeHigh", 0)
                            if total_amount > 0 and (
                                    average_price > 0 and (max_price == 0 or average_price <= max_price)):
                                delete = input(
                                    f"Enter [D] if you would like to delete your current {stock_info[1]} holdings and replace it with your inputs or [ANY OTHER KEY] to add your inputs to your current holdings\n").lower()
                                if delete.strip() == "d":
                                    db_clear_symbol(symbol, cursor, connection)
                                    direct_purchase = [(total_amount, average_price)]
                                    db_assign(symbol, cursor, connection, direct_purchase)
                                    print(f"You successfully replaced your {stock_info[1]} previous average holdings")
                                else:
                                    direct_purchase = [(total_amount, average_price)]
                                    db_assign(symbol, cursor, connection, direct_purchase)
                                    print(f"You successfully added to your current {stock_info[1]} holdings")
                            else:
                                print(f"Make sure you enter a proper price of {stock_info[1]}")
                                continue
                except ValueError:
                    print("Make sure to enter a valid number!")
                connection.commit()
        case "5":
            my_portfolio = Portfolio(db)
            rows = my_portfolio.get_grouped_stocks()
            df_reset(cursor, connection)
            connection.commit()
        case _:
            break
print("See you soon!")
