#!/usr/bin/env python3

import os
import yfinance as yf
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from InquirerPy import inquirer
from rich.prompt import IntPrompt
import pandas as pd
import numpy as np

console = Console()

MARKETVISOR_LOGO = """
[bold magenta]MVISOR  v1.0.1 by nxrev
 /$$      /$$ /$$    /$$ /$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$ 
| $$$    /$$$| $$   | $$|_  $$_/ /$$__  $$ /$$__  $$| $$__  $$
| $$$$  /$$$$| $$   | $$  | $$  | $$  \__/| $$  \ $$| $$  \ $$
| $$ $$/$$ $$|  $$ / $$/  | $$  |  $$$$$$ | $$  | $$| $$$$$$$/
| $$  $$$| $$ \  $$ $$/   | $$   \____  $$| $$  | $$| $$__  $$
| $$\  $ | $$  \  $$$/    | $$   /$$  \ $$| $$  | $$| $$  \ $$
| $$ \/  | $$   \  $/    /$$$$$$|  $$$$$$/|  $$$$$$/| $$  | $$
|__/     |__/    \_/    |______/ \______/  \______/ |__/  |__/
[bold yellow]Financial Interface Orchestration System[/bold yellow]
"""

def fetch_stock_data(symbol, period="1mo", interval="1d"):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period, interval=interval)
        return hist
    except Exception as e:
        console.print(f"Failed to fetch data: {e}", style="bold red")
        return None

def calculate_indicators(data, indicators):
    if 'SMA' in indicators:
        window = int(indicators['SMA'])
        data['SMA'] = data['Close'].rolling(window=window).mean()
    if 'EMA' in indicators:
        span = int(indicators['EMA'])
        data['EMA'] = data['Close'].ewm(span=span, adjust=False).mean()
    if 'RSI' in indicators:
        window = int(indicators['RSI'])
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        data['RSI'] = 100 - (100 / (1 + rs))
    if 'MACD' in indicators:
        exp1 = data['Close'].ewm(span=12, adjust=False).mean()
        exp2 = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = exp1 - exp2
    return data

def display_stock_data(data, symbol):
    if data.empty:
        console.print(f"No data found for {symbol}", style="bold red")
    else:
        console.print(f"Data for {symbol}:", style="bold green")
        console.print(data[['Close', 'SMA', 'EMA', 'RSI', 'MACD']].dropna().head(), style="bold blue")

def save_data(data, path):
    try:
        data.to_csv(path)
        console.print("Data has been saved successfully.", style="bold green")
    except Exception as e:
        console.print(f"Failed to save data: {e}", style="bold red")

def validate_file_path(path):
    return os.path.exists(os.path.dirname(path)) and os.access(os.path.dirname(path), os.W_OK)

def get_indicator_config(prompt_message, default_value):
    """ Helper function to configure each indicator with input validation. """
    return IntPrompt.ask(
        prompt_message,
        default=default_value,
        show_default=True,
        show_choices=False,
        validate=lambda value: value > 0,
        error_message="Please enter a positive integer."
    )

def indicators_menu():
    console.print("\n[bold cyan]Indicator Configuration Menu[/bold cyan]")
    indicators = {}
    
    if Confirm.ask("[bold cyan]Configure Simple Moving Average (SMA)?[/bold cyan]"):
        window = get_indicator_config("[bold cyan]Enter window size for SMA:[/bold cyan]", 20)
        indicators['SMA'] = window
    
    if Confirm.ask("[bold cyan]Configure Exponential Moving Average (EMA)?[/bold cyan]"):
        span = get_indicator_config("[bold cyan]Enter span for EMA:[/bold cyan]", 20)
        indicators['EMA'] = span
    
    if Confirm.ask("[bold cyan]Configure Relative Strength Index (RSI)?[/bold cyan]"):
        window = get_indicator_config("[bold cyan]Enter window size for RSI:[/bold cyan]", 14)
        indicators['RSI'] = window
    
    if Confirm.ask("[bold cyan]Would you like to configure MACD with custom EMAs?[/bold cyan]"):
        short_ema = get_indicator_config("[bold cyan]Enter short period EMA for MACD:[/bold cyan]", 12)
        long_ema = get_indicator_config("[bold cyan]Enter long period EMA for MACD:[/bold cyan]", 26)
        indicators['MACD'] = {'short_ema': short_ema, 'long_ema': long_ema}
    elif Confirm.ask("[bold cyan]Use default MACD settings?[/bold cyan]", default=True):
        indicators['MACD'] = {'short_ema': 12, 'long_ema': 26}
    
    return indicators

def data_extraction_menu():
    symbol = Prompt.ask("[bold cyan]Enter the stock symbol[/bold cyan]")
    period = inquirer.select(
        message="[bold cyan]Select the period for fetching data[/bold cyan]",
        choices=["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"]
    ).execute()
    interval = inquirer.select(
        message="[bold cyan]Select the interval between data points[/bold cyan]",
        choices=["1d", "1wk", "1mo"]
    ).execute()
    save = Confirm.ask("[bold cyan]Do you want to save the data after displaying?[/bold cyan]")
    path = ""
    if save:
        path = inquirer.text(
            message="[bold cyan]Enter the path to save the data:[/bold cyan]",
            validate=validate_file_path
        ).execute()
    return symbol, period, interval, save, path

def fetch_and_display_data(symbol, period, interval, indicators):
    console.print("Fetching stock data...", style="bold yellow")
    data = fetch_stock_data(symbol, period, interval)
    if data is not None:
        data = calculate_indicators(data, indicators)
        display_stock_data(data, symbol)
    return data

def main_menu():
    return inquirer.select(
        message="Select a Module:",
        choices=["Data Extraction", "Indicators", "Reset", "Exit"],
        default="Data Extraction"
    ).execute()

def main():
    console.print(MARKETVISOR_LOGO)
    indicators = {}  # Initialize indicators dictionary
    while True:
        action = main_menu()
        if action == 'Data Extraction':
            symbol, period, interval, save, path = data_extraction_menu()
            data = fetch_and_display_data(symbol, period, interval, indicators)
            if save and data is not None:
                save_data(data, path)
        elif action == 'Indicators':
            indicators = indicators_menu()
            console.print("Indicators configured.", style="bold green")
        elif action == 'Reset':
            console.clear()
            console.print(MARKETVISOR_LOGO)
            indicators = {}  # Reset indicators
        elif action == 'Exit':
            console.print("Exiting MarketVisor. Goodbye!", style="bold yellow")
            break

if __name__ == "__main__":
    main()
