import yfinance as yf
import logging
from database import Database
from stock import currency_symbols
from portfolio import Portfolio
from search import get_stock, get_details
from flask import Flask, jsonify, request
from flask_cors import CORS

logging.getLogger("yfinance").setLevel(logging.CRITICAL)  # blocks non-critical errors like 404 when user inputs invalid ticker


app = Flask(__name__)
CORS(app)
currency = "GBP"
db = Database()

@app.route("/portfolio", methods= ["POST"])
def portfolio():
    data = request.get_json()
    global currency
    currency = data.get("currency", "GBP")
    my_portfolio = Portfolio(db)
    grouped_stocks = my_portfolio.get_grouped_stocks()
    if not grouped_stocks:
        return jsonify({"status": 404, "data": []})
    average_price = my_portfolio.price_average(grouped_stocks)
    db_data = my_portfolio.display_portfolio(average_price, currency, currency_symbols)
    print(db_data)
    return jsonify({"data": db_data, "status": 200})


def display_currency(currency_symbols):
    display_cur = input("Enter the currency you would like to view your portfolio in e.g 'GBP' or 'USD'\n").upper()
    while display_cur not in currency_symbols.keys():
        print("Enter a valid currency or type [Q] to quit")
        display_cur = input("Enter the currency you would like to view your portfolio in e.g 'GBP' or 'USD'\n").upper()
        if display_cur == "Q":
            return display_cur
    return display_cur

choices_options = {"Declare a stock purchase to track on your portfolio": "1",
                   "Declare a stock sell to track on your portfolio": "2",
                   "Check my portfolio progress": "3",
                   "Declare the total amount you invested and the average price of your stock if available": "4",
                   "Reset your portfolio": "5"}

if __name__ == "__main__":
    app.run(port = 5000, debug=True)
    
    