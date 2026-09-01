from stock import currency_symbols
from stock import Stock

class Portfolio:
    def __init__(self, db_obj):
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
    
    def display_portfolio(self, average_price):  # calculates percentage change based on live data
        for stock in average_price:
            stock_ticker = Stock(stock[1])
            display_name = stock_ticker.ticker_obj.info.get("displayName", stock[1])
            if stock[1] in currency_symbols:
                currency = currency_symbols[stock[1]]
            else:
                cur = stock_ticker.ticker_obj.info.get("currency", "USD")
                currency = currency_symbols.get(cur,
                                                cur)  # cur, cur falls back on the currency if the symbol isnt found
            if stock[0] == 0 or stock[2] <= 0:
                print(f"You have sold all of your {display_name} shares the current holdings is {currency}0.00")
                continue
            else:
                current_price = stock_ticker.get_current_price()
                
                if current_price is None:
                    print(f"Sorry we couldn't fetch the data for {display_name} right now\nPlease try again later")
                    continue
                
                current_price = round(current_price, 2)
                percentage_change = round(((current_price - stock[0]) / stock[0]) * 100, 2)
                word = "up +" if (percentage_change / 100) > 0 else "down "
                print(
                    f"{display_name} is {word}{percentage_change}% your current holdings in {display_name} is {currency}{(current_price * stock[2]):.2f}")
