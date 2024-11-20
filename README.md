# S&P 500 Stock Heatmap Generator

A Python script that generates a heatmap visualization of S&P 500 stocks' daily returns. The heatmap provides an intuitive way to visualize stock market performance across multiple companies over time.

## Features

- Fetches real-time S&P 500 stock data using yfinance
- Generates a color-coded heatmap of stock returns
- Handles missing data and invalid stock symbols
- Processes stocks in batches to optimize API calls
- Shows last 30 days of market performance by default

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd StockHeatMap
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

Run the script:
```bash
python stockHeatMap.py
```

The script will:
1. Fetch the latest S&P 500 stock list from Wikipedia
2. Download stock price data for the last 30 days
3. Generate and display a heatmap where:
   - Green cells indicate positive returns
   - Red cells indicate negative returns
   - Yellow cells indicate neutral/small changes

## Requirements

- Python 3.9+
- pandas
- yfinance
- seaborn
- matplotlib
- numpy

## Color Scheme

The heatmap uses a Red-Yellow-Green (RYG) color scheme:
- Dark Red: Significant negative returns
- Light Red: Moderate negative returns
- Yellow: Neutral or small changes
- Light Green: Moderate positive returns
- Dark Green: Significant positive returns

## Contributing

Feel free to fork the repository and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.
