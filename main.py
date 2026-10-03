import yfinance as yf
import logging
from database import Database
from stock import currency_symbols
from portfolio import Portfolio
from search import get_stock, get_details
from flask import Flask, render_template

logging.getLogger("yfinance").setLevel(logging.CRITICAL)  # blocks non-critical errors like 404 when user inputs invalid ticker

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("portfolio.html")

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

db = Database()

if __name__ == "__main__":
    app.run(debug=True)
    
    