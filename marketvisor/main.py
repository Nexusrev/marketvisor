import yfinance as yf
from rich.console import Console
import argparse
import pandas as pd

console = Console()

MARKETVISOR_LOGO = """
 /$$      /$$ /$$    /$$ /$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$ 
| $$$    /$$$| $$   | $$|_  $$_/ /$$__  $$ /$$__  $$| $$__  $$
| $$$$  /$$$$| $$   | $$  | $$  | $$  \__/| $$  \ $$| $$  \ $$
| $$ $$/$$ $$|  $$ / $$/  | $$  |  $$$$$$ | $$  | $$| $$$$$$$/
| $$  $$$| $$ \  $$ $$/   | $$   \____  $$| $$  | $$| $$__  $$
| $$\  $ | $$  \  $$$/    | $$   /$$  \ $$| $$  | $$| $$  \ $$
| $$ \/  | $$   \  $/    /$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$
|__/     |__/    \_/    |______/ \______/  \______/ |__/  |__/
"""

def fetch_stock_data(symbol, period="1mo", interval="1d"):
    stock = yf.Ticker(symbol)
    hist = stock.history(period=period, interval=interval)
    return hist

def calculate_sma(data, window=20):
    return data['Close'].rolling(window=window).mean()

def display_stock_data(data, symbol, sma):
    if data.empty:
        console.print(f"No data found for {symbol}", style="bold red")
    else:
        console.print(f"Data for {symbol}:", style="bold green")
        console.print(data[['Close', 'SMA']].tail(), style="bold blue")  # Show the most recent data with SMA

def setup_arg_parser():
    parser = argparse.ArgumentParser(description='MarketVisor Financial CLI')
    parser.add_argument('-s', '--symbol', type=str, required=True, help='Stock symbol to fetch data for')
    parser.add_argument('-p', '--period', type=str, default='1mo', help='Period for fetching data (1mo, 3mo, 6mo, 1y, 2y, 5y, 10y)')
    parser.add_argument('-i', '--interval', type=str, default='1d', help='Interval between data points (1d, 1wk, 1mo)')
    parser.add_argument('-w', '--window', type=int, default=20, help='Window size for SMA calculation')
    return parser

def main():
    console.print(MARKETVISOR_LOGO, style="bold magenta")
    parser = setup_arg_parser()
    args = parser.parse_args()

    console.print("Fetching stock data...\n", style="bold yellow")
    data = fetch_stock_data(args.symbol, args.period, args.interval)
    data['SMA'] = calculate_sma(data, args.window)
    display_stock_data(data, args.symbol, data['SMA'])

if __name__ == "__main__":
    main()
