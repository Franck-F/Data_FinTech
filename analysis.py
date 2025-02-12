import pandas as pd
import numpy as np

def compute_ratios(symbol):
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    if "Close" not in df.columns:
        print(f"❌ Erreur : La colonne 'Close' n'existe pas dans {symbol}.csv.")
        return None

    df["Returns"] = df["Close"].pct_change()

    sharpe_ratio = np.mean(df["Returns"]) / np.std(df["Returns"]) * np.sqrt(252)
    volatility = np.std(df["Returns"]) * np.sqrt(252)

    print(f"{symbol} - Sharpe Ratio: {sharpe_ratio:.2f}, Volatilité: {volatility:.2%}")

if __name__ == "__main__":
    for asset in ["BTC", "SP500", "GOLD"]:
        compute_ratios(asset)
