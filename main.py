from re import A
import requests
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from data_fetcher import fetch_data
from alerts import plot_trends  # Correction ici !
from stats_analysis import plot_daily_returns, plot_return_distribution, plot_volatility, plot_drawdown, compute_var  # Ajout ici
from correlation import plot_correlation_matrix
from predictor import plot_forecast
from visualization import plot_price_trends, plot_comparison, plot_candlestick_2, plot_comparison_percentage
from indicators import plot_bollinger_bands, plot_macd, plot_rsi
from visualization import plot_candlestick
from forex_python.converter import CurrencyRates



# Fonction de conversion avec gestion des erreurs et alternative API
def convertir_devise(montant, devise_source, devise_cible):
    try:
        # Tentative d'utilisation de forex_python
        c = CurrencyRates()
        taux = c.get_rate(devise_source, devise_cible)
        return montant * taux
    except Exception as e:
        # Si forex_python échoue, utiliser une API alternative
      #st.warning("Erreur avec l'API Forex Python. Tentative d'utilisation d'une autre API.")
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{devise_source}"
            response = requests.get(url)
            data = response.json()
            taux = data['rates'].get(devise_cible, 1)
            return montant * taux
        except Exception as e:
            st.error(f"Erreur API : {e}")
            return montant  # Retourner le montant initial si tout échoue

 
# 🌟 Interface Streamlit
st.set_page_config(page_title="Analyse Financière", layout="wide")

# Mise en page du titre
st.markdown(
    """
    <h1 style='text-align: center; font-family: Signika, sans-serif; font-weight: bold;'>
        Dashboard financier 📈
    </h1>
    """, unsafe_allow_html=True
)
 
col_1, col_2 = st.columns([2, 1])
with col_1: 
    st.subheader("📊 Analyse des Actifs")
with col_2:
    if st.button("📊 Analyse"):
        st.switch_page("pages/analyse") 
    st.button("Rapport", key="rapport_button")
    
   
#  Sélection de l'actif
col1, col2 = st.columns([2, 1])
with col1:
     actif = st.selectbox("Sélectionnez un actif 🏦", ["BTC", "SP500", "GOLD"])
with col2:
    devise = st.selectbox("Sélectionnez la devise 💸", ["USD", "EUR", "GBP"])
    prix_usd = 1  # Exemple
    prix_converti = convertir_devise(prix_usd, "USD", devise)
 
# Définir la couleur en fonction de la devise
    if devise == "USD":
      couleur = "orange"
    elif devise == "EUR":
     couleur = "blue"
    else:
     couleur = "magenta"
     
 
# Afficher le prix avec la couleur appropriée
    st.write(f"Prix en <span style='color:{couleur}'>{devise}</span> : <span style='color:{couleur}'>{prix_converti:.2f} {devise}</span>", unsafe_allow_html=True)

# Options de filtres
filters = st.multiselect("Sélectionnez les filtres à appliquer :", ["RSI", "MACD", "Rendement", "SMA", "EMA"])

# --- Section Overview ---
tab_overview, tab_details, tab_comparison, tab_risques = st.tabs(["Overview", "Details", "Comparaison", "Risques"])

with tab_overview:  
    # 📈 Graphique en Chandeliers
    st.subheader("📈 Evolution des prix des actifs")
    plot_candlestick(actif)

with tab_details:
    # 📊 Analyse des Indicateurs
    st.subheader("📈 Evolution des prix des actifs")
    plot_candlestick_2(actif, filters)  
     
    # 🛑 RSI (Indicateur Technique)
    st.subheader("🛑 Indicateur Technique : RSI")
    plot_rsi(actif)

    # 📊 Bandes de Bollinger
    st.subheader("📊 Bandes de Bollinger")
    plot_bollinger_bands(actif)

    # 📉 MACD (Moving Average Convergence Divergence)
    st.subheader("📉 MACD")
    plot_macd(actif)
   
    # 📈 Graphique d'Évolution des Prix avec Moyenne Mobile
    st.subheader("📉 Évolution des Prix avec Moyenne Mobile")
    plot_price_trends(actif)
    
    # 📊 Distribution des Rendements
    st.subheader("📊 Distribution des Rendements Quotidiens")
    plot_return_distribution(actif)
    
    # 📊 Volatilité Annuelle
    st.subheader("📊 Volatilité Annuelle")
    plot_volatility()
    
     # 📉 Rendements Quotidiens
    st.subheader("📉 Rendements Quotidiens")
    plot_daily_returns(actif)
        
    # 🏹 Prédiction des Prix
    st.subheader("🏹 Prédiction des Prix (30 jours)")
    plot_forecast(actif)

with tab_comparison:
    # 📊 Comparaison des Actifs
    st.subheader("Comparaison des actifs ")
    plot_comparison()
    plot_comparison_percentage()
    

with tab_risques:
    # 🚨 Risques associés aux actifs
    st.markdown(
    "<h1 style='text-align: center;'>📊 Analyse des Risques Financiers</h1>", 
    unsafe_allow_html=True)
    # 📉 VaR
    compute_var(actif)

    # 📉 Drawdown
    plot_drawdown(actif)
    

