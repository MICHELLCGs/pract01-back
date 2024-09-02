import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json

# Paso 1: Descargar el archivo CSV
url = 'https://myawsbucketmichell.s3.sa-east-1.amazonaws.com/people.csv'  # URL original, ajusta si es necesario
filename = 'people.csv'
response = requests.get(url)

# Guardar el archivo CSV
with open(filename, 'wb') as file:
    file.write(response.content)

# Paso 2: Leer el CSV
df = pd.read_csv(filename)

# Ver las primeras filas del dataframe para identificar columnas relevantes
print(df.head())

# Seleccionamos la columna que contiene el texto a procesar
# Ajusta según la columna correcta de tu CSV
text_column = 'name'  # Reemplaza con la columna correcta de tu CSV

# Aplicar TF-IDF para convertir el texto en vectores numéricos
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df[text_column])

# Calcular la similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Mostrar la matriz de similitud
print(cosine_sim)

# Función para obtener las recomendaciones
def get_recommendations(index, cosine_sim, df, text_column):
    # Obtener las puntuaciones de similitud para el índice dado
    sim_scores = list(enumerate(cosine_sim[index]))
    
    # Ordenar las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtener los índices de los cursos más similares
    sim_scores = sim_scores[1:6]  # Tomar los 5 más similares, omitir el mismo curso
    
    # Obtener los índices
    course_indices = [i[0] for i in sim_scores]
    
    # Retornar los cursos similares
    return df.iloc[course_indices]

# Ejemplo: obtener recomendaciones para el primer registro
index_to_check = 0
recommendations = get_recommendations(index_to_check, cosine_sim, df, text_column)

# Reemplazar NaN con pd.NA
recommendations = recommendations.where(pd.notnull(recommendations), None)

# Convertir las recomendaciones en un diccionario con una clave
recommendations_dict = {"recommendations": recommendations.to_dict(orient='records')}

# Crear la carpeta 'Data' si no existe
output_folder = './pract04/Data'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Guardar el JSON en la carpeta 'Data'
output_file = os.path.join(output_folder, 'recommendations.json')
with open(output_file, 'w') as file:
    json.dump(recommendations_dict, file, indent=4)

print(f"Recomendaciones guardadas en {output_file}")
