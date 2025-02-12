import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
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
    

def compute_var(symbol, confidence_level=0.95):
    """Calcule la Value at Risk (VaR) pour un actif donné."""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)    
    # Calcul des rendements quotidiens
    df["Daily_Return"] = df["Close"].pct_change()    
    # Suppression des valeurs NaN
    returns = df["Daily_Return"].dropna()
    # Vérification s'il reste des valeurs après suppression
    if returns.empty:
        return np.nan, f"⚠️ Impossible de calculer la VaR pour {symbol} (pas assez de données)."
    # Calcul de la VaR
    var = np.percentile(returns, (1 - confidence_level) * 100)
    st.markdown(f"### 📉 Value at Risk (VaR) - {symbol}")
    st.write(f"🔻 La VaR à {confidence_level*100:.0f}% indique qu'un investisseur pourrait perdre au maximum "
             f"**{abs(var):.2%}** sur une journée en conditions normales de marché.")
    return var

def plot_drawdown(symbol):
    """Calcule et affiche le drawdown maximum sous forme de graphique."""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)
    df["Cumulative_Return"] = (1 + df["Close"].pct_change()).cumprod()
    df["Peak"] = df["Cumulative_Return"].cummax()
    df["Drawdown"] = (df["Cumulative_Return"] - df["Peak"]) / df["Peak"]

    max_drawdown = df["Drawdown"].min()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Drawdown"], 
                             mode='lines', name="Drawdown",
                             line=dict(color="red")))
    
    fig.update_layout(title=f"📉 Drawdown Historique de {symbol}",
                      xaxis_title="Date",
                      yaxis_title="Drawdown (%)",
                      hovermode="x unified")
    
    st.markdown(f"### 📉 Drawdown Maximum - {symbol}")
    st.write(f"📉 **Drawdown Maximal : {max_drawdown:.2%}** (perte maximale observée depuis un sommet)")
    
    st.plotly_chart(fig, use_container_width=True)

def plot_return_distribution(symbol):
    """Affiche la distribution des rendements quotidiens avec un histogramme interactif."""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)
    df["Daily_Return"] = df["Close"].pct_change().dropna()

    fig = px.histogram(df, x="Daily_Return", nbins=50, 
                       title=f"Distribution des Rendements Quotidiens ({symbol})",
                       labels={"Daily_Return": "Rendement"},
                       marginal="box", opacity=0.75)
    
    st.plotly_chart(fig, use_container_width=True)

def plot_daily_returns(symbol):
    """Affiche les rendements quotidiens sous forme de courbe interactive."""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)
    df["Daily_Return"] = df["Close"].pct_change().dropna()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Daily_Return"], 
                             mode='lines', name=f"Rendements {symbol}",
                             line=dict(color="blue")))
    
    fig.update_layout(title=f"Rendements Quotidiens de {symbol}",
                      xaxis_title="Date",
                      yaxis_title="Rendement",
                      hovermode="x unified")
    
    st.plotly_chart(fig, use_container_width=True)

def plot_volatility():
    """Affiche la volatilité annuelle des actifs sous forme de graphique interactif."""
    assets = ["BTC", "SP500", "GOLD"]
    volatilities = []

    for asset in assets:
        df = pd.read_csv(f"data/{asset}.csv", index_col=0, parse_dates=True)
        daily_volatility = df["Close"].pct_change().std()
        annual_volatility = daily_volatility * np.sqrt(252)
        volatilities.append(annual_volatility)

    df_vol = pd.DataFrame({"Actifs": assets, "Volatilité Annuelle": volatilities})

    fig = px.bar(df_vol, x="Actifs", y="Volatilité Annuelle", 
                 title="Comparaison de la Volatilité Annuelle",
                 color="Actifs", text_auto='.2%',
                 labels={"Volatilité Annuelle": "Volatilité (%)"})
    
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    print("⚠ Ce script est conçu pour être utilisé avec Streamlit.")
