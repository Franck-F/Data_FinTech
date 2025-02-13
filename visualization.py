import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np 

def plot_price_trends(symbol):
    """Affiche l'évolution des prix avec la moyenne mobile (SMA 20)"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)
    df["SMA_20"] = df["Close"].rolling(window=20).mean()

    # Création du graphique
    fig = px.line(df, x=df.index, y=["Close", "SMA_20"],
                  title=f"Tendances de {symbol}",
                  labels={"value": "Prix", "index": "Date"},
                  template="plotly_dark")

    # Affichage avec Streamlit
    st.plotly_chart(fig)

def plot_candlestick(symbol):
    """Affiche un graphique en chandeliers avec histogramme de volatilité annuelle"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calcul des rendements journaliers et de la volatilité
    df["Return"] = df["Close"].pct_change()
    df["Volatility"] = df["Return"].rolling(window=30).std() * np.sqrt(252)

    # Création d'un subplot avec deux graphiques, avec une plus grande proportion pour le chandelier
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.4, 
                           row_heights=[0.85, 0.15], 
                           subplot_titles=(f"Evolution des prix {symbol}", "Volatilité Annuelle"))

    # Ajout du graphique en chandeliers
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Prix"
    ), row=1, col=1)

    # Ajout de l'histogramme de volatilité
    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volatility"],
        name="Volatilité Annuelle",
        marker_color="red"
    ), row=2, col=1)

    # Mise en forme
    fig.update_layout(
        height=500,  # Augmente la hauteur globale du graphique
        xaxis_title="Date",
        yaxis_title="Prix",
        showlegend=False
    )


    # Affichage avec Streamlit
    st.plotly_chart(fig)
def plot_comparison():
    """Affiche l'évolution des prix normalisés des 3 actifs avec échelle logarithmique"""
    # Chargement des données
    df_sp500 = pd.read_csv("data/SP500.csv", index_col=0, parse_dates=True)
    df_btc = pd.read_csv("data/BTC.csv", index_col=0, parse_dates=True)
    df_gold = pd.read_csv("data/GOLD.csv", index_col=0, parse_dates=True)

    # Normalisation des prix pour une comparaison claire
    df_sp500["Normalized"] = df_sp500["Close"] / df_sp500["Close"].iloc[0]
    df_btc["Normalized"] = df_btc["Close"] / df_btc["Close"].iloc[0]
    df_gold["Normalized"] = df_gold["Close"] / df_gold["Close"].iloc[0]

    # Transformation logarithmique
    df_sp500["Log_Normalized"] = np.log(df_sp500["Normalized"])
    df_btc["Log_Normalized"] = np.log(df_btc["Normalized"])
    df_gold["Log_Normalized"] = np.log(df_gold["Normalized"])

    # Création du graphique
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_sp500.index, y=df_sp500["Log_Normalized"], mode="lines",
                             name="S&P 500", line=dict(color="gold")))
    fig.add_trace(go.Scatter(x=df_btc.index, y=df_btc["Log_Normalized"], mode="lines",
                             name="BTC", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=df_gold.index, y=df_gold["Log_Normalized"], mode="lines",
                             name="GOLD", line=dict(color="blue")))

    # Ajout des étiquettes finales sur la dernière valeur de chaque actif
    last_date = df_sp500.index[-1]
    fig.add_trace(go.Scatter(x=[last_date], y=[df_sp500["Log_Normalized"].iloc[-1]],
                             text=["S&P 500"], mode="text",
                             textposition="middle right", textfont=dict(color="gold", size=14)))

    fig.add_trace(go.Scatter(x=[last_date], y=[df_btc["Log_Normalized"].iloc[-1]],
                             text=["BTC"], mode="text",
                             textposition="middle right", textfont=dict(color="green", size=14)))

    fig.add_trace(go.Scatter(x=[last_date], y=[df_gold["Log_Normalized"].iloc[-1]],
                             text=["GOLD"], mode="text",
                             textposition="middle right", textfont=dict(color="blue", size=14)))

    # Mise en forme
    fig.update_layout(
        title="Comparaison de l'évolution des prix (Logarithmique)",
        xaxis_title="Date",
        yaxis_title="Log(Prix normalisé)",
        template="plotly_white",
        showlegend=False
    )

    # Affichage avec Streamlit
    st.plotly_chart(fig)

    
    
def plot_comparison_percentage():
    """Affiche l'évolution des prix en pourcentage (%) depuis le premier jour."""
    # Chargement des données
    df_sp500 = pd.read_csv("data/SP500.csv", index_col=0, parse_dates=True)
    df_btc = pd.read_csv("data/BTC.csv", index_col=0, parse_dates=True)
    df_gold = pd.read_csv("data/GOLD.csv", index_col=0, parse_dates=True)

    # Calcul des performances en pourcentage par rapport au premier jour
    df_sp500["Perf_%"] = (df_sp500["Close"] / df_sp500["Close"].iloc[0] - 1) * 100
    df_btc["Perf_%"] = (df_btc["Close"] / df_btc["Close"].iloc[0] - 1) * 100
    df_gold["Perf_%"] = (df_gold["Close"] / df_gold["Close"].iloc[0] - 1) * 100

    # Création du graphique
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_sp500.index, y=df_sp500["Perf_%"], mode="lines",
                             name="S&P 500", line=dict(color="gold")))
    fig.add_trace(go.Scatter(x=df_btc.index, y=df_btc["Perf_%"], mode="lines",
                             name="BTC", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=df_gold.index, y=df_gold["Perf_%"], mode="lines",
                             name="GOLD", line=dict(color="blue")))

    # Ajout des étiquettes finales sur la dernière valeur de chaque actif
    last_date = df_sp500.index[-1]
    fig.add_trace(go.Scatter(x=[last_date], y=[df_sp500["Perf_%"].iloc[-1]],
                             text=["S&P 500"], mode="text",
                             textposition="middle right", textfont=dict(color="gold", size=14)))

    fig.add_trace(go.Scatter(x=[last_date], y=[df_btc["Perf_%"].iloc[-1]],
                             text=["BTC"], mode="text",
                             textposition="middle right", textfont=dict(color="green", size=14)))

    fig.add_trace(go.Scatter(x=[last_date], y=[df_gold["Perf_%"].iloc[-1]],
                             text=["GOLD"], mode="text",
                             textposition="middle right", textfont=dict(color="blue", size=14)))

    # Mise en forme
    fig.update_layout(
        title="Comparaison des performances des actifs (%)",
        xaxis_title="Date",
        yaxis_title="Performance depuis le début (%)",
        template="plotly_white",
        showlegend=False
    )

    # Affichage avec Streamlit
    st.plotly_chart(fig)

#================================================ DETAILS =====================================================#

#=========================fonction de calcul des indicateurs

    
def calculate_indicators(df, filters):
    """Calcule les indicateurs techniques sélectionnés."""
    if "RSI" in filters:
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))

    if "MACD" in filters:
        df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
        df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()
        df["MACD"] = df["EMA_12"] - df["EMA_26"]
        df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    if "SMA" in filters:
        df["SMA_50"] = df["Close"].rolling(window=50).mean()
        df["SMA_200"] = df["Close"].rolling(window=200).mean()

    if "EMA" in filters:
        df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()
        df["EMA_200"] = df["Close"].ewm(span=200, adjust=False).mean()

    return df

#===============================================================================================================
#================================== Affichage

def plot_candlestick_2(symbol, filters):
    """Affiche un graphique en chandeliers avec histogramme de volatilité annuelle et indicateurs techniques sélectionnés."""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calcul des rendements et volatilité
    df["Return"] = df["Close"].pct_change()
    df["Volatility"] = df["Return"].rolling(window=30).std() * np.sqrt(252)

    # Appliquer les calculs des indicateurs techniques
    df = calculate_indicators(df, filters)

    # Création d'un subplot
    fig = sp.make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.15,
                           row_heights=[0.85, 0.15], 
                           subplot_titles=(f"Evolution des prix {symbol}", "Volatilité Annuelle"))

    # Ajout du graphique en chandeliers
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Prix"
    ), row=1, col=1)

    # Ajout des indicateurs sélectionnés
    colors = {"SMA": "blue", "EMA": "purple", "MACD": "green", "RSI": "orange"}

    if "SMA" in filters:
        fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"], mode="lines", line=dict(color="blue", width=1), name="SMA 50"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["SMA_200"], mode="lines", line=dict(color="blue", width=1, dash="dot"), name="SMA 200"), row=1, col=1)

    if "EMA" in filters:
        fig.add_trace(go.Scatter(x=df.index, y=df["EMA_50"], mode="lines", line=dict(color="purple", width=1), name="EMA 50"), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["EMA_200"], mode="lines", line=dict(color="purple", width=1, dash="dot"), name="EMA 200"), row=1, col=1)

    if "MACD" in filters:
        fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], mode="lines", line=dict(color="green", width=1), name="MACD"), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["MACD_Signal"], mode="lines", line=dict(color="red", width=1), name="MACD Signal"), row=2, col=1)

    if "RSI" in filters:
        fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode="lines", line=dict(color="orange", width=1), name="RSI"), row=2, col=1)

    # Ajout de l'histogramme de volatilité
    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volatility"],
        name="Volatilité Annuelle",
        marker_color="red"
    ), row=2, col=1)

    # Mise en forme
    fig.update_layout(
        height=800,
        xaxis_title="Date",
        yaxis_title="Prix",
        showlegend=True
    )

    st.plotly_chart(fig) 
    
#====================================================fin================================================================

if __name__ == "__main__":
    print("⚠ Ce script est conçu pour être utilisé avec Streamlit.")

