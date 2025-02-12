import os
import pandas as pd
import yfinance as yf

ASSETS = {
    "BTC": "BTC-USD",
    "SP500": "^GSPC",
    "GOLD": "GC=F"
}

def fetch_data(symbol):
    """Télécharge et nettoie les données Yahoo Finance"""
    if symbol not in ASSETS:
        print(f"❌ Actif {symbol} non reconnu.")
        return None

    data = yf.download(ASSETS[symbol], period="6y")

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    data = data[["Open", "High", "Low", "Close", "Volume"]]

    os.makedirs("data", exist_ok=True)
    file_path = f"data/{symbol}.csv"
    data.to_csv(file_path)

    return data

if __name__ == "__main__":
    for asset in ASSETS.keys():
        fetch_data(asset)
