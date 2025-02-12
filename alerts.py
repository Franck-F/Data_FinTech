import pandas as pd
import plotly.graph_objects as go

def plot_trends(symbol):
    print(f"📊 Affichage des tendances pour {symbol}...")

    try:
        df = pd.read_csv(f"data/{symbol}.csv", index_col=0, parse_dates=True)
    except FileNotFoundError:
        print(f"❌ Erreur : Fichier {symbol}.csv introuvable.")
        return None

    if "Close" not in df.columns:
        print(f"❌ Erreur : La colonne 'Close' est absente dans {symbol}.csv.")
        return None

    df["SMA_20"] = df["Close"].rolling(window=20).mean()
    df["Diff"] = (df["Close"] - df["SMA_20"]) / df["SMA_20"] * 100

    # Séparer les périodes de forte hausse/baisse
    df["Trend"] = "Stable"
    df.loc[df["Diff"] > 5, "Trend"] = "Hausse"
    df.loc[df["Diff"] < -5, "Trend"] = "Baisse"

    # Création du graphique interactif
    fig = go.Figure()

    # Courbe du prix
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Prix", line=dict(color="blue")))

    # Moyenne mobile
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"], mode="lines", name="Moyenne Mobile 20j", line=dict(color="orange")))

    # Points de forte hausse
    df_up = df[df["Trend"] == "Hausse"]
    fig.add_trace(go.Scatter(
        x=df_up.index, y=df_up["Close"],
        mode="markers", name="Forte Hausse",
        marker=dict(color="green", size=8, symbol="triangle-up")
    ))

    # Points de forte baisse
    df_down = df[df["Trend"] == "Baisse"]
    fig.add_trace(go.Scatter(
        x=df_down.index, y=df_down["Close"],
        mode="markers", name="Forte Baisse",
        marker=dict(color="red", size=8, symbol="triangle-down")
    ))

    # Mise en page
    fig.update_layout(
        title=f"Tendances de {symbol}",
        xaxis_title="Date",
        yaxis_title="Prix",
        legend_title="Légende",
        template="plotly_white"
    )

    fig.show()

if __name__ == "__main__":
    for asset in ["BTC", "SP500", "GOLD"]:
        plot_trends(asset)
