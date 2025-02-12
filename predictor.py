from prophet import Prophet
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


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
