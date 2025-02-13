import streamlit as st
import pdfkit
from predictor import plot_forecast
from visualization import plot_price_trends, plot_comparison, plot_candlestick_2, plot_comparison_percentage
from indicators import plot_bollinger_bands, plot_macd, plot_rsi
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from data_fetcher import fetch_data
from alerts import plot_trends  # Correction ici !
from stats_analysis import plot_daily_returns, plot_return_distribution, plot_volatility, plot_drawdown, compute_var  # Ajout ici
from correlation import plot_correlation_matrix
from visualization import plot_price_trends, plot_comparison, plot_candlestick_2, plot_comparison_percentage
from visualization import plot_candlestick
from forex_python.converter import CurrencyRates
import pdfkit
from io import BytesIO
import plotly.io as pio
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO



# 🌟 Interface Streamlit
st.set_page_config(page_title="Analyse Financière", layout="wide")
actif = st.selectbox("Sélectionnez un actif 🏦", ["BTC", "SP500", "GOLD"])
# Options de filtres
filters = st.multiselect("Sélectionnez les filtres à appliquer :", ["RSI", "MACD", "Rendement", "SMA", "EMA"])

# Mise en page du titre
st.markdown(
    """
    <h1 style='text-align: center; font-family: Signika, sans-serif; font-weight: bold;'>
        Analyse Globale 📈
    </h1>
    """, unsafe_allow_html=True
)
 
# 📈 Évolution des prix sous forme de chandeliers japonais
st.subheader("📈 Evolution des prix des actifs")
st.markdown(
    """
    Ce graphique en chandeliers japonais montre les variations de prix de l'actif sélectionné sur une période donnée. 
    Il permet d'identifier les tendances haussières et baissières en analysant les patterns de prix. 
    Les chandeliers japonais sont un outil essentiel pour les traders techniques, car ils fournissent des informations 
    visuelles sur les mouvements de prix, les niveaux de support et de résistance, ainsi que les signaux potentiels de 
    retournement de tendance.
    """
)
plot_candlestick(actif)

st.subheader("📈 Evolution des prix des actifs avec filtres")
st.markdown("Ce graphique avancé intègre plusieurs indicateurs techniques sélectionnés pour affiner davantage l'analyse des tendances de marché.")
plot_candlestick_2(actif, filters)  
     
# 🎭 Indicateur Technique : RSI
st.subheader("🎭 Indicateur Technique : RSI")
st.markdown("L'indice de force relative (RSI) mesure la vitesse et le changement des mouvements de prix. Un RSI supérieur à 70 indique une surachat, tandis qu'un RSI inférieur à 30 signale une survente. Cet indicateur est particulièrement utile pour identifier les conditions de marché extrêmes et les points potentiels de retournement de tendance.")
plot_rsi(actif)

# 🌊 Bandes de Bollinger
st.subheader("🌊 Bandes de Bollinger")
st.markdown(
    """
    Les bandes de Bollinger illustrent la volatilité du marché en traçant une enveloppe autour des prix basée sur la moyenne mobile et l'écart-type. 
    Elles sont composées de trois lignes : la bande supérieure, la bande inférieure et la moyenne mobile simple (SMA) au milieu. 
    La bande supérieure est calculée en ajoutant un multiple de l'écart-type à la SMA, tandis que la bande inférieure est obtenue en soustrayant ce multiple de l'écart-type à la SMA. 
    Les bandes de Bollinger sont utilisées pour identifier les conditions de surachat et de survente, ainsi que pour détecter les périodes de forte volatilité. 
    Lorsque les prix se rapprochent de la bande supérieure, l'actif est considéré comme suracheté, et lorsqu'ils se rapprochent de la bande inférieure, il est considéré comme survendu.
    """
)
plot_bollinger_bands(actif)

# 📉 MACD (Moving Average Convergence Divergence)
st.subheader("📉 MACD")
st.markdown(
    """
    Le MACD (Moving Average Convergence Divergence) est un indicateur de momentum qui met en évidence la relation entre deux moyennes mobiles d'un actif. 
    Il est utilisé pour identifier les tendances et les points d'entrée/sortie du marché. 
    Le MACD est composé de deux lignes : la ligne MACD (différence entre deux moyennes mobiles exponentielles) et la ligne de signal (moyenne mobile exponentielle de la ligne MACD). 
    Un croisement de la ligne MACD au-dessus de la ligne de signal est généralement interprété comme un signal d'achat, tandis qu'un croisement en dessous est considéré comme un signal de vente.
    """
)
plot_macd(actif)
   
# 📈 Graphique d'Évolution des Prix avec Moyenne Mobile
st.subheader("📉 Évolution des Prix avec Moyenne Mobile")
st.markdown("Ce graphique affiche la tendance des prix en intégrant des moyennes mobiles, permettant de lisser davantage les fluctuations du marché et de détecter les tendances sous-jacentes.")
plot_price_trends(actif)
    
# 🌊 Distribution des Rendements
st.subheader("🌊 Distribution des Rendements Quotidiens")
st.markdown(
    """
    Ce graphique présente la répartition des rendements quotidiens d'un actif, utile pour évaluer la fréquence des variations et détecter les événements extrêmes. 
    En analysant cette distribution, les investisseurs peuvent mieux comprendre la volatilité de l'actif et identifier les périodes de forte instabilité. 
    Cela permet également de repérer les rendements anormaux qui pourraient indiquer des opportunités ou des risques potentiels. 
    Une distribution symétrique autour de zéro suggère un équilibre entre les gains et les pertes, tandis qu'une distribution asymétrique peut signaler une tendance haussière ou baissière.
    """
)
plot_return_distribution(actif)
    
# 🌊 Volatilité Annuelle
st.subheader("🌊 Volatilité Annuelle")
st.markdown("La volatilité annuelle mesure les fluctuations des prix sur une base annuelle, offrant un aperçu plus approfondi du niveau de risque de l'actif étudié.")
plot_volatility()
    
# 📉 Rendements Quotidiens
st.subheader("📉 Rendements Quotidiens")
st.markdown(
    """
    Les rendements quotidiens permettent d'analyser la performance journalière d'un actif et de détecter les périodes de forte variation. 
    En observant les rendements quotidiens, les investisseurs peuvent identifier les tendances à court terme et évaluer la volatilité de l'actif. 
    Cela aide également à repérer les anomalies ou les événements spécifiques qui ont un impact significatif sur les prix. 
    Une analyse détaillée des rendements quotidiens peut fournir des informations précieuses pour la prise de décision en matière d'investissement et de gestion des risques.
    """
)
plot_daily_returns(actif)
        
# 🏉 Prédiction des Prix
st.subheader("🏉 Prédiction des Prix (30 jours)")
st.markdown("Cette section présente une projection des prix de l'actif sur les 30 prochains jours en se basant sur des modèles prédictifs, permettant ainsi d'anticiper les tendances futures et de prendre des décisions d'investissement plus éclairées.")
plot_forecast(actif)

# 🌊 Comparaison des Actifs
st.subheader("Comparaison des actifs")
st.markdown("Cette section permet de comparer les performances de plusieurs actifs afin d'identifier les plus rentables ou les plus stables.")
plot_comparison()
plot_comparison_percentage()
    
# 🚨 Risques associés aux actifs
st.markdown(
    "<h1 style='text-align: center;'>🌊 Analyse des Risques Financiers</h1>", 
    unsafe_allow_html=True)

# 📉 Value at Risk (VaR)
st.markdown("La Value at Risk (VaR) évalue le risque de perte potentiel d'un actif sur une période donnée, avec un niveau de confiance spécifique. Cet indicateur est essentiel pour quantifier le risque de marché et pour la gestion des portefeuilles d'investissement.")
compute_var(actif)

# 📉 Drawdown
st.markdown("Le drawdown représente la perte maximale enregistrée à partir d'un sommet jusqu'à un creux, offrant un indicateur clé du risque de perte en capital. En analysant le drawdown, les investisseurs peuvent mieux comprendre les périodes de pertes importantes et ajuster leurs stratégies de gestion des risques en conséquence.")
plot_drawdown(actif)



# 📌 Générer un PDF avec les graphiques et les analyses
def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y_position = height - 50  # Position initiale

    # Sommaire avec liens interactifs
    toc = [
        ("📈 Évolution des prix", "plot_candlestick.png"),
        ("🎭 Indicateur RSI", "plot_rsi.png"),
        ("🌊 Bandes de Bollinger", "plot_bollinger.png"),
        ("📉 MACD", "plot_macd.png"),
        ("📊 Distribution des Rendements", "plot_return_dist.png"),
        ("📈 Volatilité Annuelle", "plot_volatility.png"),
        ("📉 Rendements Quotidiens", "plot_daily_returns.png"),
        ("🏉 Prédiction des Prix", "plot_forecast.png"),
        ("🔗 Corrélations entre actifs", "plot_correlation_matrix.png"),
        ("📉 Drawdown", "plot_drawdown.png"),
    ]

    # 📌 Génération du sommaire
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y_position, "📌 Sommaire")
    y_position -= 30
    c.setFont("Helvetica", 12)

    for i, (title, img) in enumerate(toc):
        c.drawString(70, y_position, f"{i+1}. {title}")
        c.linkURL(f"#{title}", (50, y_position-5, 250, y_position+10))
        y_position -= 20

    c.showPage()  # Nouvelle page après le sommaire
    y_position = height - 50

    # 📌 Génération des graphiques et ajout dans le PDF
    figures = {
        "plot_candlestick.png": plot_candlestick,
        "plot_rsi.png": plot_rsi,
        "plot_bollinger.png": plot_bollinger_bands,
        "plot_macd.png": plot_macd,
        "plot_return_dist.png": plot_return_distribution,
        "plot_volatility.png": plot_volatility,
        "plot_daily_returns.png": plot_daily_returns,
        "plot_forecast.png": plot_forecast,
        "plot_correlation_matrix.png": plot_correlation_matrix,
        "plot_drawdown.png": plot_drawdown
    }

    for title, img_name in toc:
        if img_name in figures:
            try:
                fig = figures[img_name]("BTC")  # Modifier selon l'actif sélectionné
                if fig is not None:
                    img_buffer = BytesIO()
                    fig.write_image(img_buffer, format="png")  # Sauvegarde en mémoire
                    img_buffer.seek(0)

                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(50, y_position, title)
                    y_position -= 20

                    img = ImageReader(img_buffer)
                    c.drawImage(img, 50, y_position - 200, width=500, height=200, preserveAspectRatio=True, anchor='c')
                    y_position -= 250

                    if y_position < 100:
                        c.showPage()  # Nouvelle page si besoin
                        y_position = height - 50
                else:
                    print(f"Erreur : Le graphique '{img_name}' est vide ou invalide.")
            except Exception as e:
                print(f"Erreur lors de la génération du graphique {title}: {e}")


    c.save()
    buffer.seek(0)
    return buffer

# 📩 Bouton pour télécharger le PDF
if st.button("📥 Télécharger le rapport PDF"):
    pdf_file = generate_pdf()
    st.download_button(
        label="📥 Télécharger",
        data=pdf_file,
        file_name="Rapport_Analyse.pdf",
        mime="application/pdf"
    )
