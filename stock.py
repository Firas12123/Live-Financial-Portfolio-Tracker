import yfinance as yf
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

class Stock:
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.ticker_obj = yf.Ticker(self.ticker)
    
    def get_current_price(self):
        current_data = self.ticker_obj.history(period="1d")
        if current_data.empty:
            return None
        return current_data["Close"].iloc[-1]