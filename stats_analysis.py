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
    
    # Définition des couleurs pour chaque actif
    colors = {"BTC": "green", "GOLD": "gold", "SP500": "blue"}
    
    # Chargement des données
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)
    df["Daily_Return"] = df["Close"].pct_change().dropna()

    # Création du graphique avec la couleur spécifique de l'actif
    fig = px.histogram(df, x="Daily_Return", nbins=50, 
                       title=f"Distribution des Rendements ({symbol})",
                       labels={"Daily_Return": "Rendement"},
                       marginal="box", opacity=0.75,
                       color_discrete_sequence=[colors.get(symbol, "gray")])  # Couleur par défaut : gris

    # Affichage avec Streamlit
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
    colors = {"BTC": "green", "SP500": "blue", "GOLD": "gold"}  # Définition des couleurs
    volatilities = []
    
    for asset in assets:
        df = pd.read_csv(f"data/{asset}.csv", index_col=0, parse_dates=True)
        daily_volatility = df["Close"].pct_change().std()
        annual_volatility = daily_volatility * np.sqrt(252)  # Conversion en volatilité annuelle
        volatilities.append(annual_volatility)

    df_vol = pd.DataFrame({"Actifs": assets, "Volatilité Annuelle": volatilities})

    # Création du graphique avec les couleurs spécifiques
    fig = px.bar(df_vol, x="Actifs", y="Volatilité Annuelle", 
                 title="Comparaison de la Volatilité (5 années cumulées)",
                 text_auto='.2%', 
                 labels={"Volatilité Annuelle": "Volatilité (%)"},
                 color="Actifs", color_discrete_map=colors)  # Mapping des couleurs
    
    # Affichage avec Streamlit
    st.plotly_chart(fig, use_container_width=True)


def load_data(file_path):
    """Charge les données depuis un fichier CSV et calcule les rendements."""
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    df['Return'] = df['Close'].pct_change()  # Rendement sous forme décimale
    return df

def plot_annual_volatility():
    """Affiche la volatilité annuelle des actifs (Bitcoin, S&P 500, Or) regroupée par année."""
    # Chargement des données
    df_sp500 = load_data("data/SP500.csv")
    df_btc = load_data("data/BTC.csv")
    df_gold = load_data("data/GOLD.csv")

    # Resampling des données pour obtenir les rendements annuels
    df_sp500_annual_volatility = df_sp500['Return'].resample('Y').std()  # Calcul de la volatilité annuelle
    df_btc_annual_volatility = df_btc['Return'].resample('Y').std()
    df_gold_annual_volatility = df_gold['Return'].resample('Y').std()

    # Création des années de référence
    years = df_sp500_annual_volatility.index.year

    # Préparer les volatilités pour l'affichage
    df_volatility = pd.DataFrame({
        "Year": years,
        "S&P 500": df_sp500_annual_volatility.values,
        "Bitcoin": df_btc_annual_volatility.values,
        "Gold": df_gold_annual_volatility.values
    })

    # Création du graphique
    fig = go.Figure()

    # Ajouter les traces pour chaque actif avec des couleurs dynamiques
    colors = {"S&P 500": "blue", "Bitcoin": "green", "Gold": "gold"}
    for asset in df_volatility.columns[1:]:
        fig.add_trace(go.Bar(x=df_volatility["Year"], y=df_volatility[asset], name=asset, marker_color=colors[asset]))

    # Mise en forme du graphique
    fig.update_layout(
        title="Volatilité Annuelle des Actifs",
        xaxis_title="Année",
        yaxis_title="Volatilité Annuelle (Écart-type)",
        barmode="group",  # Regroupement des barres
        template="plotly_white",
        showlegend=True,
        yaxis=dict(
            tickmode='array',  # Utiliser un mode d'échelle personnalisé
            tickvals=[i/100 for i in range(int(df_volatility[['S&P 500', 'Bitcoin', 'Gold']].min().min()*100), int(df_volatility[['S&P 500', 'Bitcoin', 'Gold']].max().max()*100)+1)],
            ticktext=[f'{i/100:.2f}' for i in range(int(df_volatility[['S&P 500', 'Bitcoin', 'Gold']].min().min()*100), int(df_volatility[['S&P 500', 'Bitcoin', 'Gold']].max().max()*100)+1)]
        )
    )

    # Affichage avec Streamlit
    st.plotly_chart(fig)

def plot_annual_returns():
    """Affiche les rendements annuels des actifs (Bitcoin, S&P 500, Or) regroupés par année."""
    # Chargement des données
    df_sp500 = load_data("data/SP500.csv")
    df_btc = load_data("data/BTC.csv")
    df_gold = load_data("data/GOLD.csv")

    # Resampling des données pour obtenir les rendements annuels
    df_sp500_annual_returns = df_sp500['Return'].resample('Y').sum()  # Somme des rendements annuels
    df_btc_annual_returns = df_btc['Return'].resample('Y').sum()
    df_gold_annual_returns = df_gold['Return'].resample('Y').sum()

    # Création des années de référence
    years = df_sp500_annual_returns.index.year

    # Préparer les rendements pour l'affichage
    df_returns = pd.DataFrame({
        "Year": years,
        "S&P 500": df_sp500_annual_returns.values,
        "Bitcoin": df_btc_annual_returns.values,
        "Gold": df_gold_annual_returns.values
    })

    # Création du graphique
    fig = go.Figure()

    # Ajouter les traces pour chaque actif avec des couleurs dynamiques
    colors = {"S&P 500": "blue", "Bitcoin": "green", "Gold": "gold"}
    for asset in df_returns.columns[1:]:
        fig.add_trace(go.Bar(x=df_returns["Year"], y=df_returns[asset], name=asset, marker_color=colors[asset]))

    # Mise en forme du graphique
    fig.update_layout(
        title="Rendements Annuels des Actifs",
        xaxis_title="Année",
        yaxis_title="Rendement Annuel",
        barmode="group",  # Regroupement des barres
        template="plotly_white",
        showlegend=True
    )

    # Affichage avec Streamlit
    st.plotly_chart(fig)


if __name__ == "__main__":
    print("⚠ Ce script est conçu pour être utilisé avec Streamlit.")
