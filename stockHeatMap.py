import pandas as pd
import ssl
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configuration
CONFIG = {
    'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),  # Last 30 days
    'end_date': datetime.now().strftime('%Y-%m-%d'),
    'sp500_url': 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
}

def fix_stock_symbol(symbol):
    """Fix common stock symbol issues."""
    # Handle special cases
    if symbol == 'BRK.B':
        return 'BRK-B'
    if symbol == 'BF.B':
        return 'BF-B'
    return symbol.replace('.', '-')

def get_sp500_tickers():
    """Fetch S&P 500 tickers from Wikipedia."""
    try:
        # Read all tables from Wikipedia page
        tables = pd.read_html(CONFIG['sp500_url'])
        # The S&P 500 companies table is the first table
        df = tables[0]
        # Get the ticker symbols and clean them
        tickers = df['Symbol'].tolist()
        # Fix ticker symbols
        tickers = [fix_stock_symbol(ticker) for ticker in tickers]
        return tickers
    except Exception as e:
        print(f"Error fetching S&P 500 tickers: {e}")
        return []

def get_valid_tickers(ticker_symbols, batch_size=20):
    """Filter out invalid tickers and fetch data in batches."""
    valid_tickers = []
    
    # Process tickers in batches
    for i in range(0, len(ticker_symbols), batch_size):
        batch = ticker_symbols[i:i + batch_size]
        try:
            # Download data for the batch
            data = yf.download(
                batch,
                start=CONFIG['start_date'],
                end=CONFIG['end_date'],
                progress=False,
                group_by='ticker'
            )
            
            # If single ticker, data structure is different
            if len(batch) == 1:
                if not data.empty:
                    valid_tickers.append(batch[0])
            else:
                # Check which tickers have data
                for ticker in batch:
                    try:
                        if not data[ticker]['Adj Close'].empty:
                            valid_tickers.append(ticker)
                    except KeyError:
                        continue
                        
        except Exception as e:
            print(f"Error processing batch: {e}")
            continue
            
    return valid_tickers

def create_heatmap(valid_tickers):
    """Create and display the stock price percentage changes heatmap."""
    try:
        # Download data for valid tickers
        all_data = yf.download(
            valid_tickers,
            start=CONFIG['start_date'],
            end=CONFIG['end_date'],
            progress=False
        )['Adj Close']
        
        # Calculate daily percentage change
        percentage_change = all_data.pct_change().dropna()
        
        # Create heatmap
        plt.figure(figsize=(20, 12))
        sns.heatmap(percentage_change, 
                    annot=False, 
                    cmap="RdYlGn",  # Red for negative, Yellow for neutral, Green for positive
                    center=0,
                    robust=True)  # Makes the colormap robust against outliers
        
        plt.title("S&P 500 Stocks Daily Returns Heatmap (Last 30 Days)")
        plt.xlabel("Stocks")
        plt.ylabel("Date")
        
        # Rotate x-axis labels for better readability
        plt.xticks(rotation=90)
        plt.tight_layout()  # Adjust layout to prevent label cutoff
        
        plt.show()
        
    except Exception as e:
        print(f"Error creating heatmap: {e}")

def main():
    """Main function to orchestrate the heatmap creation process."""
    # Bypass SSL certificate verification (if needed)
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # Get and process tickers
    print("Fetching S&P 500 tickers...")
    ticker_symbols = get_sp500_tickers()
    if not ticker_symbols:
        print("Failed to fetch S&P 500 tickers.")
        return
    
    print(f"Found {len(ticker_symbols)} tickers. Getting valid tickers...")
    # Get valid tickers
    valid_tickers = get_valid_tickers(ticker_symbols)
    if not valid_tickers:
        print("No valid tickers available for analysis.")
        return
    
    print(f"Processing {len(valid_tickers)} valid tickers...")
    # Create and display heatmap
    create_heatmap(valid_tickers)

if __name__ == "__main__":
    main()
