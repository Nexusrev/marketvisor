#!/usr/bin/env python3

import yfinance as yf
from rich.console import Console
import argparse
import pandas as pd
from InquirerPy import prompt
from InquirerPy.validator import NumberValidator
import termplotlib as tpl

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

A Financial CLI Framework
Author: arkadiaanalytics
Codename: nexusrev
Version: 1.0.1#beta
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
        data['SMA'] = sma
        console.print(data[['Open', 'Close', 'Volume', 'SMA']].tail(), style="bold blue")  # Display additional data points
        fig = tpl.figure()
        fig.plot(data['Close'].tail(10).index, data['Close'].tail(10), width=50, height=15, xlabel="Date", title="Closing Prices")
        fig.show()

def interactive_menu():
    questions = [
        {
            'type': 'input',
            'name': 'symbol',
            'message': 'Enter the stock symbol:',
            'validate': lambda result: True if result else "This field cannot be empty."
        },
        {
            'type': 'list',
            'name': 'period',
            'message': 'Select the period for fetching data:',
            'choices': ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y']
        },
        {
            'type': 'list',
            'name': 'interval',
            'message': 'Select the interval between data points:',
            'choices': ['1d', '1wk', '1mo']
        },
        {
            'type': 'input',
            'name': 'window',
            'message': 'Enter the window size for SMA calculation:',
            'validate': NumberValidator("Please enter a valid number")
        }
    ]
    return prompt(questions)

def main():
    console.print(MARKETVISOR_LOGO, style="bold magenta")
    user_input = interactive_menu()
    console.print("Fetching stock data...\n", style="bold yellow")
    data = fetch_stock_data(user_input['symbol'], user_input['period'], user_input['interval'])
    sma = calculate_sma(data, int(user_input['window']))
    display_stock_data(data, user_input['symbol'], sma)

if __name__ == "__main__":
    main()
