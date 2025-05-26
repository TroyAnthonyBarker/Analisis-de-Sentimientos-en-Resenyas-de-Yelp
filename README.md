# Análisis de Opiniones de Clientes en Yelp

## Descripción
Análisis de reseñas de Yelp mediante técnicas de NLP y visualización para identificar sentimientos, patrones y percepciones del cliente. El objetivo es generar insights útiles para la mejora de servicios y estrategias empresariales.

## Objetivos
- Analizar el contenido textual de reseñas de Yelp a gran escala.
- Detectar el sentimiento general de los usuarios.
- Identificar temas y patrones comunes en las opiniones.
- Ofrecer visualizaciones claras y accionables.
- Generar recomendaciones basadas en datos para la mejora de servicios.

## Dataset
- **Nombre**: `yelp_review_full`
- **Fuente**: [Hugging Face Datasets](https://huggingface.co/datasets/yelp_review_full)
- Contiene 650.000 reseñas con puntuación de 1 a 5 estrellas.

## Herramientas utilizadas
- Python 3.12.9
- Pandas y NumPy
- Matplotlib y Seaborn / Plotly
- Scikit-learn
- NLTK o spaCy
- Transformers
- Jupyter Notebook

## Estructura del proyecto
```
📁 Analisis-de-Sentimientos-en-Resenyas-de-Yelp
├── notebooks/
│   └── analisis.ipynb
│   └── preparacion_de_datos.ipynb
├── src/
│   └── descarga.py
│   └── visualizacion.py
├── README.md
├── requirements.txt
```

## Cómo ejecutar
1. Clona el repositorio.
2. Instala los paquetes requeridos:
   ```
   pip install -r requirements.txt
   ```
3. Ejecuta el script `src\descarga.py`
4. Ejecuta los notebooks en `notebooks/` paso a paso.
5. Ejecuta el script con streamlit `src\visualizacion.py`

## Posibles mejoras futuras
- Incorporación de modelos de lenguaje como BERT o RoBERTa.

## Licencia
Este proyecto se distribuye bajo la licencia MIT.
