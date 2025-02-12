import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def compute_financial_metrics(symbol):
    """Calcule rendement quotidien, annuel, volatilité et ratios"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calcul du rendement quotidien
    df["Daily_Return"] = df["Close"].pct_change()

    # Calcul du rendement annuel moyen
    annual_return = df["Daily_Return"].mean() * 252

    # Volatilité annuelle (écart-type des rendements)
    annual_volatility = df["Daily_Return"].std() * np.sqrt(252)

    # Sharpe Ratio (on suppose un taux sans risque de 2%)
    risk_free_rate = 0.02
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility

    # Sortino Ratio (ne prend en compte que les pertes)
    negative_returns = df["Daily_Return"][df["Daily_Return"] < 0]
    downside_volatility = negative_returns.std() * np.sqrt(252)
    sortino_ratio = (annual_return - risk_free_rate) / downside_volatility if downside_volatility > 0 else np.nan

    print(f"\n🔹 {symbol} - Analyse Financière")
    print(f"📈 Rendement Annuel Moyen : {annual_return:.2%}")
    print(f"📉 Volatilité Annuelle : {annual_volatility:.2%}")
    print(f"⚖ Sharpe Ratio : {sharpe_ratio:.2f}")
    print(f"📊 Sortino Ratio : {sortino_ratio:.2f}")

def plot_return_distribution(symbol):
    """Affiche la distribution des rendements quotidiens"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)
    df["Daily_Return"] = df["Close"].pct_change()

    # Création du graphique
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["Daily_Return"].dropna(), bins=50, kde=True, ax=ax)
    ax.set_title(f"Distribution des Rendements Quotidiens ({symbol})")
    ax.set_xlabel("Rendement")
    ax.set_ylabel("Fréquence")

    # Affichage avec Streamlit
    st.pyplot(fig)

def plot_daily_returns(symbol):
    """Affiche les rendements quotidiens sous forme de courbe"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)
    df["Daily_Return"] = df["Close"].pct_change()

    # Création du graphique
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df["Daily_Return"], label=f"Rendements {symbol}", color="blue")
    ax.axhline(0, color='black', linestyle='--')
    ax.set_title(f"Rendements Quotidiens de {symbol}")
    ax.legend()

    # Affichage avec Streamlit
    st.pyplot(fig)
def plot_volatility():
    """Affiche la volatilité annuelle des actifs"""
    assets = ["BTC", "SP500", "GOLD"]
    volatilities = []

    for asset in assets:
        df = pd.read_csv(f"data/{asset}.csv", index_col=0, parse_dates=True)
        daily_volatility = df["Close"].pct_change().std()
        annual_volatility = daily_volatility * np.sqrt(252)
        volatilities.append(annual_volatility)

    # Création du graphique
    df_vol = pd.DataFrame({"Actifs": assets, "Volatilité Annuelle": volatilities})
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x="Actifs", y="Volatilité Annuelle", data=df_vol, ax=ax)
    ax.set_title("Comparaison de la Volatilité Annuelle")
    ax.set_ylabel("Volatilité (%)")

    # Affichage avec Streamlit
    st.pyplot(fig)

if __name__ == "__main__":
    print("⚠ Ce script est conçu pour être utilisé avec Streamlit.")
