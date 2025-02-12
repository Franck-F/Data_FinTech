import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def plot_bollinger_bands(symbol):
    """Affiche les Bandes de Bollinger pour un actif"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calcul des bandes de Bollinger
    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["STD_20"] = df["Close"].rolling(window=20).std()
    df["Upper_Band"] = df["SMA_20"] + (df["STD_20"] * 2)
    df["Lower_Band"] = df["SMA_20"] - (df["STD_20"] * 2)

    # Création du graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode='lines', name="Prix"))
    fig.add_trace(go.Scatter(x=df.index, y=df["Upper_Band"], mode='lines', name="Bande Supérieure", line=dict(color="red")))
    fig.add_trace(go.Scatter(x=df.index, y=df["Lower_Band"], mode='lines', name="Bande Inférieure", line=dict(color="green")))

    fig.update_layout(title=f"Bandes de Bollinger pour {symbol}", xaxis_title="Date", yaxis_title="Prix")

    # Affichage avec Streamlit
    st.plotly_chart(fig)

def plot_macd(symbol):
    """Affiche le MACD pour un actif"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calcul du MACD
    df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA_12"] - df["EMA_26"]
    df["Signal_Line"] = df["MACD"].ewm(span=9, adjust=False).mean()

    # Création du graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], mode='lines', name="MACD"))
    fig.add_trace(go.Scatter(x=df.index, y=df["Signal_Line"], mode='lines', name="Ligne de Signal", line=dict(color="red")))

    fig.update_layout(title=f"MACD pour {symbol}", xaxis_title="Date", yaxis_title="Valeur MACD")

    # Affichage avec Streamlit
    st.plotly_chart(fig)

def plot_rsi(symbol):
    """Affiche le RSI de l'actif avec Streamlit"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calcul du RSI
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Création du graphique
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], mode='lines', name="RSI", line=dict(color="purple")))
    fig.add_trace(go.Scatter(x=df.index, y=[70] * len(df), mode='lines', name="Surachat (70)", line=dict(color="red", dash="dash")))
    fig.add_trace(go.Scatter(x=df.index, y=[30] * len(df), mode='lines', name="Survente (30)", line=dict(color="green", dash="dash")))

    fig.update_layout(title=f"RSI pour {symbol}", xaxis_title="Date", yaxis_title="RSI")

    # Affichage avec Streamlit
    st.plotly_chart(fig)
    
    
    

    
    

if __name__ == "__main__":
    print("⚠ Ce script est conçu pour être utilisé avec Streamlit.")
