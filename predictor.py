from prophet import Prophet
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

def predict_and_plot(asset_data, features, target='Clôture', plot_title='Prédiction des Clôtures'):
    """Fonction de prédiction pour un actif donné et visualisation des résultats"""
    
    # Séparation des données
    X = asset_data[features]  # Variables indépendantes
    y = asset_data[target]  # Variable cible
    
    # Séparation des données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Modèle de régression linéaire
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Prédiction sur l'ensemble de test
    y_pred = model.predict(X_test)
    
    # Calcul des scores de validation croisée
    scores = cross_val_score(model, X, y, cv=5, scoring='neg_mean_squared_error')
    rmse_mean = np.mean(np.sqrt(-scores))
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Affichage des résultats
    st.write(f"RMSE moyen (validation croisée) : {rmse_mean:.4f}")
    st.write(f"MSE sur les données de test : {mse:.4f}")
    st.write(f"R² sur les données de test : {r2:.4f}")
    
    # Visualisation des résultats
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.index, y_test, label='Valeurs réelles', color='blue')
    plt.plot(y_pred, label='Prédictions', color='red')
    plt.title(plot_title)
    plt.legend()
    
    # Affichage dans Streamlit
    st.pyplot()

def main():
    # Charger les données dans df_total
    df_gold = pd.read_csv("data/GOLD.csv")
    df_btc = pd.read_csv("data/BTC.csv")
    df_sp500 = pd.read_csv("data/SP500.csv")
    # Assurez-vous que vos données sont chargées dans df_total
    # Exemple de données pour un actif, ici l'Or
    gold_data = df_gold[df_gold['Actif'] == 'Or'].dropna(subset=['Clôture', 'RSI', 'Rendement', 'Haut', 'Bas', 'Ouverture', 'Volatilité'])
    
    features = ["Ouverture", "Haut", "Bas", "RSI", "Volatilité", "Rendement"]
    
    # Prédiction et affichage des résultats pour chaque actif
    st.title("Prédiction des Prix des Actifs")
    
    # Bitcoin
    bitcoin_data = df_btc[df_btc['Actif'] == 'Bitcoin'].dropna(subset=['Clôture', 'RSI', 'Rendement', 'Haut', 'Bas', 'Ouverture', 'Volatilité'])
    st.subheader("Bitcoin")
    predict_and_plot(bitcoin_data, features, plot_title='Prédiction de la Clôture - Bitcoin')
    
    # Or
    st.subheader("Or")
    predict_and_plot(gold_data, features, plot_title='Prédiction de la Clôture - Or')
    
    # S&P 500
    sp500_data = df_sp500[df_sp500['Actif'] == 'S&P 500'].dropna(subset=['Clôture', 'RSI', 'Rendement', 'Haut', 'Bas', 'Ouverture', 'Volatilité'])
    st.subheader("S&P 500")
    predict_and_plot(sp500_data, features, plot_title='Prédiction de la Clôture - S&P 500')

def plot_forecast(symbol):
    """Affiche les prévisions des prix avec Prophet"""
    df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)

    # Renommer les colonnes pour Prophet
    df = df.rename(columns={"Close": "y"})
    df["ds"] = df.index

    # Entraînement du modèle Prophet
    model = Prophet()
    model.fit(df)

    # Création des prévisions sur 30 jours
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Création du graphique avec Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["ds"], y=df["y"], mode='lines', name="Historique"))
    fig.add_trace(go.Scatter(x=forecast["ds"], y=forecast["yhat"], mode='lines', name="Prévision"))
    fig.update_layout(title=f"Prédictions de {symbol} (30 jours)", xaxis_title="Date", yaxis_title="Prix")

    # Vérifie si on est dans Streamlit avant d'afficher
    try:
        st.plotly_chart(fig)
    except RuntimeError:
        print("⚠ Attention : Exécute ce script avec Streamlit (`streamlit run main.py`).")


if __name__ == "__main__":
    print("⚠ Ce script est conçu pour être utilisé avec Streamlit.")
