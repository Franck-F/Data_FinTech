import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


def plot_correlation_matrix():
    """Affiche la matrice de corrélation entre BTC, SP500 et OR avec Streamlit"""
    assets = ["BTC", "SP500", "GOLD"]
    data = {asset: pd.read_csv(f"data/{asset}.csv", index_col=0, parse_dates=True)["Close"] for asset in assets}

    df = pd.DataFrame(data)
    correlation_matrix = df.corr()

    # Affichage avec Seaborn
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    plt.title("Matrice de Corrélation entre Actifs")

    # Affichage dans Streamlit
    st.pyplot(fig)


if __name__ == "__main__":
    plot_correlation_matrix()
