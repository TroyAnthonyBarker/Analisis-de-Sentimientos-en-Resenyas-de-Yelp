import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from utils import sentiment_classifier

# Configuración
st.set_page_config(page_title="Análisis de Sentimientos", layout="wide")

filename = "./data/yelp_reviews_classified.csv"

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv(filename)

df = load_data()

# Navegacion
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Go to",                             # Texto arriba de las opciones
    ["Data", "Explore", "Visualizations", "Sentiment Analyst"]
)

# Separador
st.sidebar.markdown('---')

# Filtros
st.sidebar.header("Filtros")

sentimientos = st.sidebar.multiselect(
    "Selecciona sentimiento", options=df['sentimiento'].unique(), default=df['sentimiento'].unique()
)

min_star, max_star = int(df['stars'].min()), int(df['stars'].max())
stars_range = st.sidebar.slider("Filtra por puntuación (stars)", min_star, max_star, (min_star, max_star))

# Aplicar filtros
df_filtrado = df[(df['sentimiento'].isin(sentimientos)) & (df['stars'].between(*stars_range))]

st.header("📊 Análisis de Sentimientos en Reseñas de Yelp")

if page == "Data":
    st.subheader('⚙️ Raw Data')
    col1, col2 = st.columns(2)

    # Métricas
    with col1:
        st.metric("Total de reseñas", len(df_filtrado))
    with col2:
        st.metric("Promedio de puntuación", round(df_filtrado['stars'].mean(), 2))
    
    # Reseñas
    st.subheader("Reseñas")
    st.dataframe(df_filtrado[['review', 'sentimiento', 'stars']].reset_index(drop=True).head(10), use_container_width=True)

elif page == "Explore":
    st.subheader("🌐 Exploración de Datos")
    # Reseñas
    st.subheader("Reseñas")
    st.dataframe(df_filtrado[['review', 'sentimiento', 'stars']].reset_index(drop=True), use_container_width=True)

elif page == "Visualizations":
    st.subheader("👁️‍🗨️ Visualización grafica")
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
        st.subheader("Distribución por Estrellas")

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

elif page == "Sentiment Analyst":
    st.subheader("💬 Analizador de sentimientos")
    st.sidebar.markdown("---")
    
    print(st.session_state)
    if "messages" not in st.session_state or st.sidebar.button("Reset chat"):
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Input phrase..."):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        if prompt:
            try:
                sentiment = sentiment_classifier(prompt, clean=False)[0]
                response = st.write_stream([f"The phare you have provided is {sentiment["label"]} I am {"%.2f" % sentiment["score"]}% certain."])
            except Exception as e:
                response = st.write_stream([e.args[0]])
        else:
            response = st.write_stream(["Hello, write a phrase you want classifien."])

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})