from re import A
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from data_fetcher import fetch_data
from alerts import plot_trends  # Correction ici !
from stats_analysis import plot_daily_returns, plot_volatility  # Ajout ici
from correlation import plot_correlation_matrix
from predictor import plot_forecast
from indicators import plot_rsi
from visualization import plot_price_trends
from predictor import plot_forecast
from indicators import plot_rsi
from visualization import plot_price_trends
from indicators import plot_bollinger_bands, plot_macd
from stats_analysis import plot_return_distribution
from visualization import plot_candlestick
from stats_analysis import plot_daily_returns
from stats_analysis import plot_volatility
from indicators import plot_rsi




# 🌟 Interface Streamlit
st.set_page_config(page_title="Analyse Financière", layout="wide")

# Mise en page du titre
st.markdown(
    """
    <h1 style='text-align: center; font-family: Arial, sans-serif; font-weight: bold;'>
        Dashboard financier 📈
    </h1>
    """, unsafe_allow_html=True
)
 
col_1, col_2 = st.columns([2, 1])
with col_1: 
    st.title("📊 Analyse des Actifs")
with col_2:
    st.button("Analyse")
    st.button("Rapport")
   
#  Sélection de l'actif
col1, col2 = st.columns([2, 1])
with col1:
     actif = st.selectbox("Sélectionnez un actif 🏦", ["BTC", "SP500", "GOLD"])
with col2:
    devise = st.selectbox("Sélectionnez la devise 💸", ["USD", "EUR", "GBP"])

# Options de filtres
filters = st.multiselect("Sélectionnez les filtres à appliquer :", ["RSI", "MACD", "Rendement", "SMA", "EMA"])

# --- Section Overview ---
tab_overview, tab_details, tab_comparison = st.tabs(["Overview", "Details", "Comparaison"])

with tab_overview:  
    # 📈 Graphique en Chandeliers
    st.subheader("📈 Evolution des prix des actifs")
    plot_candlestick(actif)

with tab_details:
       
    # 🛑 RSI (Indicateur Technique)
    st.subheader("🛑 Indicateur Technique : RSI")
    plot_rsi(actif)

    # 📊 Bandes de Bollinger
    st.subheader("📊 Bandes de Bollinger")
    plot_bollinger_bands(actif)

    # 📉 MACD (Moving Average Convergence Divergence)
    st.subheader("📉 MACD")
    plot_macd(actif)
    
    # 📉 Rendements Quotidiens
    st.subheader("📉 Rendements Quotidiens")
    plot_daily_returns(actif)

    # 📊 Volatilité Annuelle
    st.subheader("📊 Volatilité Annuelle")
    plot_volatility()

    # 🏹 Prédiction des Prix
    st.subheader("🏹 Prédiction des Prix (30 jours)")
    plot_forecast(actif)

with tab_comparison:
# 📊 Distribution des Rendements
    st.subheader("📊 Distribution des Rendements Quotidiens")
    plot_return_distribution(actif)

    # 📈 Graphique d'Évolution des Prix avec Moyenne Mobile
    st.subheader("📉 Évolution des Prix avec Moyenne Mobile")
    plot_price_trends(actif)

