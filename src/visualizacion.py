import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Configuración
st.set_page_config(page_title="Análisis de Sentimientos Yelp", layout="wide")
st.title("📊 Análisis de Sentimientos en Reseñas de Yelp")

filename = "./data/yelp_reviews_classified.csv"

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv(filename)

df = load_data()

# Filtros
st.sidebar.header("Filtros")

sentimientos = st.sidebar.multiselect(
    "Selecciona sentimiento", options=df['sentimiento'].unique(), default=df['sentimiento'].unique()
)

min_star, max_star = int(df['stars'].min()), int(df['stars'].max())
stars_range = st.sidebar.slider("Filtra por puntuación (stars)", min_star, max_star, (min_star, max_star))

# Aplicar filtros
df_filtrado = df[(df['sentimiento'].isin(sentimientos)) & (df['stars'].between(*stars_range))]

# Métricas
st.metric("Total de reseñas", len(df_filtrado))
st.metric("Promedio de puntuación", round(df_filtrado['stars'].mean(), 2))

# Visualización
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Sentimientos")

    sentiment_counts = df_filtrado['sentimiento'].value_counts().reset_index()
    sentiment_counts.columns = ['Sentimiento', 'Cantidad']

    # Mapa de colores solo para Positivo y Negativo
    color_map = {
        "Positivo": "green",
        "Negativo": "red"
    }

    fig = px.bar(
        sentiment_counts,
        x='Cantidad',
        y='Sentimiento',
        orientation='h',
        color='Sentimiento',
        text='Cantidad',
        color_discrete_map=color_map
    )

    fig.update_traces(textposition='auto')
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)


with col2:
    st.subheader("Distribución por Estrellas (interactivo)")

    stars_counts = df_filtrado['stars'].value_counts().sort_index().reset_index()
    stars_counts.columns = ['Estrellas', 'Cantidad']

    # Convertimos a string para evitar escala continua
    stars_counts['Estrellas'] = stars_counts['Estrellas'].astype(str)

    # Definimos el orden de categorías para las estrellas
    category_order = ['0', '1', '2', '3', '4']

    # Secuencia de colores: rojo a verde
    color_sequence = ['#d73027', '#fc8d59', '#fee08b', '#91cf60', '#1a9850']

    fig2 = px.bar(
        stars_counts,
        x='Estrellas',
        y='Cantidad',
        color='Estrellas',
        text='Cantidad',
        category_orders={'Estrellas': category_order},
        color_discrete_sequence=color_sequence
    )

    fig2.update_traces(textposition='auto')
    fig2.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig2, use_container_width=True)

# Reseñas
st.subheader("Reseñas")
st.dataframe(df_filtrado[['review', 'sentimiento', 'stars']].reset_index(drop=True), use_container_width=True)