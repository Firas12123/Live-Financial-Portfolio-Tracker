# Live Financial Portfolio Tracker

A Python CLI tool for tracking stock investments locally using SQLite and real-time data from Yahoo Finance. I built this to manage buy and sell transactions cleanly without losing historical cost bases or breaking when taking profits.

## Class breakdown
* **`Database` (`Database` class):** 
  * Encapsulates SQLite connection management and automated table initialization (`Portfolio.db`).
* **`Stock` (`Stock` class):** 
  * Acts as a dedicated wrapper around the `yfinance` API. It handles stock tickers , metadata retrieval (currency, exchange, display names) for the API, and live price fetching using minute-level slicing (`period="1d"`).
* **`Portfolio` (`Portfolio` class):** 
  * Manages portfolio-level business logic. Portfolio manages live user updates, executes cost-averaging algorithms for selling and buying positions, and rendering portfolio outputs.

## What it does
- **Live Market Data:** Pulls live data for active trading days or the last price on non-trading days `yfinance`.
- **Ledger System:** Stores everything in a local SQLite database (`Portfolio.db`), logging buys as positive values and sells as negative.
- **Smart Profit Tracking:** Keeps your original average purchase price intact when you sell at a gain, meaning your ROI and percentage updates stay mathematically accurate.
- **Safe Inputs:** Built with proper error handling and loop escapes (`[M]`) so you don't get trapped if you make a typo.
- **Manual Overrides:** Lets you manually punch in your total net deposits and average broker price if you want to skip inputting every individual trade.

1. Install the Yahoo Finance dependency:
   ```bash
   pip install yfinance