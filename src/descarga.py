"""
This script downloads the Yelp Review Full dataset using the Hugging Face `datasets` library,
renames the columns for clarity, and saves the train and test splits as CSV files.

Steps performed:
1. Loads the Yelp Review Full dataset.
2. Renames the 'text' column to 'review' and the 'label' column to 'stars' in both train and test splits.
3. Saves the processed train and test datasets as CSV files in the specified data directory.

Dependencies:
- datasets (Hugging Face)

File outputs:
- ./data/yelp_reviews_train.csv
- ./data/yelp_reviews_test.csv

Author: Troy Anthony Barker
# src/descarga.py
"""

from datasets import load_dataset
import pandas as pd
import os


PATH = "./data/"

# Create the data directory if it doesn't exist
os.makedirs(PATH, exist_ok=True)

# Cargar el dataset
dataset = load_dataset("Yelp/yelp_review_full")

# Renombrar las columnas
train =  pd.DataFrame(dataset['train']).rename(columns={'text': 'review', 'label': 'stars'})
test = pd.DataFrame(dataset['test']).rename(columns={'text': 'review', 'label': 'stars'})

# Juntar los datasets train y test
df = pd.concat([train, test])

# Resetear el índice del DataFrame
# df.reset_index(inplace=True)

# Definir los nombres de los archivos
filename = PATH + 'yelp_reviews.csv'

# Guardar el dataset en un archivo CSV
df.to_csv(filename, index=False)