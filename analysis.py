import pandas as pd
import numpy as np

def compute_ratios(symbol):
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    if "Close" not in df.columns:
        print(f"❌ Erreur : La colonne 'Close' n'existe pas dans {symbol}.csv.")
        return None

    df["Returns"] = df["Close"].pct_change()

    # Ratio de Sharpe
    sharpe_ratio = np.mean(df["Returns"]) / np.std(df["Returns"]) * np.sqrt(252)

    # Volatilité annuelle
    volatility = np.std(df["Returns"]) * np.sqrt(252)

    # Rendement annuel moyen
    annual_return = (1 + df["Returns"].mean())**252 - 1

    return {
        "Sharpe Ratio": round(sharpe_ratio, 2),
        "Volatilité": round(volatility * 100, 2),
        "Rendement Annuel": round(annual_return * 100, 2)
    }

