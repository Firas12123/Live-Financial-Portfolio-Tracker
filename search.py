import requests


def get_stock(choice2, rows, currency_symbols):
    stock_info = []
    while True:  # verify if user input is a real stock name / ticker
        print("If this was a mistake type [M] to go back to the menu")
        user_currency = input("Enter the currency you have purchased your stock with e.g ('GBP', 'USD')\n").upper()
        while user_currency not in currency_symbols.keys():
            print("Enter a valid currency")
            user_currency = input(
                "Enter the currency you have purchased your stocks with e.g ('GBP', 'USD')\n").upper()
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
                        stock_info.append(stock_ticker.info.get("allTimeHigh",
                                                                0))  # not brackets as it will crash if not find so use .get so if not found it can assign 0
                        symbol_choice = search_results[stock_val].get("symbol", "N/A")
                        stock_info.append(stock_ticker.info.get("displayName", symbol_choice))
                        stock_info.append(stock_ticker.info.get("shortname", "N/A"))
                        stock_info.append(symbol_choice)
                        stock_currency = stock_ticker.info.get("currency",
                                                               "N/A")  # gets currency symbol according to the market e.g. US market = $
                        currency = currency_symbols.get(stock_currency,
                                                        stock_currency)  # falls back on the stock_currency input if symbol isn't found inside our dictionary
                        stock_info.append(currency)
                        stock_info.append(user_currency)
                        stock_info.append(stock_currency)
                        return stock_info
                    elif stock_cho > len_stk or stock_cho <= 0:
                        word = f"You only have 1 option to chose from you cant chose {stock_cho}" if len_stk == 1 else f"You must pick a number between 1-{len_stk}!"
                        print(f"{word}")
                else:
                    print(
                        "If you cant find your stock make sre your spelling is correct and adjust for any capitals")
        except Exception as e:
            print(f"Sorry the market didnt behaves expected please try again soon\nError:{e}")
            
def get_details(max_price, choice2, rows, symbol,currency, user_currency, real_currency, currency_symbols):  # get the amount invested and the price of the stock at the price invested into a list as a tuple
    x = 0
    purchases = []
    while x == 0:
        try:
            word1 = "sold" if choice2 == "2" else "bought"
            print("If you have made a mistake type [M] to return to the main menu")
            user_symbol = currency_symbols.get(user_currency)
            amount_inv = input(f"Enter the amount you have {word1} of the stock, in {user_symbol}\n").lower()
            if amount_inv.strip() == "m":
                x += 1
                return False
            user_amount = float(amount_inv)
            if user_amount > 0:
                if real_currency == user_currency:  # only mixup is between GBP and GBp which is same currency but 100x more
                    amount_invested = user_amount
                else:
                    url = f"https://api.frankfurter.dev/v1/latest?base={user_currency}&symbols={real_currency}"
                    response = requests.get(url)
                    data = response.json()
                    rate = data["rates"][real_currency]
                    amount_invested = float(user_amount) * rate
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
                                    f"You couldn't have sold at {user_currency}{amount_invested:.2f} if you had {currency}{total_value:.2f} in {symbol} at {currency}{share_price}")
                                continue
                        if share_price > 0 and (max_price == 0 or share_price <= max_price):
                            purchases.append((amount_invested, share_price))  # two brackets to store as a tuple
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
