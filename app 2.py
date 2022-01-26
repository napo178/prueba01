# Importamos 
import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from wordcloud import WordCloud

# Para obtener la lista de "stopwords" y asi descartarlas
import nltk
from nltk.corpus import stopwords

#Generación de lista de signos de puntuación
import string  

def limpiar_puntuacion_stopwords(texto):
  """
  Funcion para limpiar el string
  #Modificado de la siguiente fuente: https://antonio-fernandez-troyano.medium.com/nube-de-palabras-word-cloud-con-python-a-partir-de-varias-webs-111e94220822
  Parameters 
  ---------------
  texto (str)       -> Texto a limpiar
  Returns
  ---------------
  texto_limpio (str) -> Texto limpio luego de sacarle signos de puntuacion y stopwords
  """
  puntuacion = []
  for s in string.punctuation:
      puntuacion.append(str(s))
  sp_puntuacion = ["¿", "¡", "“", "”", "…", ":", "–", "»", "«", "?", "!"]    

  puntuacion += sp_puntuacion

  #Reemplazamos signos de puntuación por "":
  for p in puntuacion:
      texto_limpio = texto.lower().replace(p,"")

  for p in puntuacion:
      texto_limpio = texto_limpio.replace(p,"")

  #Reemplazamos stop_words por "":    
  for stop in stop_words:
      texto_limpio_lista = texto_limpio.split()
      texto_limpio_lista = [i.strip() for i in texto_limpio_lista]
      try:
          while stop in texto_limpio_lista: texto_limpio_lista.remove(stop)
      except:
          print("Error")
          pass
      texto_limpio= " ".join(texto_limpio_lista)

  return texto_limpio


def generar_nube_de_palabras(input, uploded_file = None):  
  """
  Funcion para hacer la nube de palabras en base a un .csv especifico que tenga una columna "ShareCommentary" como se encuentra
  en el archivo Share.csv que nos proporciona LinkedIn
  
  Parameters
  ------------------
  input        -> Para decidir si se usa el 'template' o se toma el archivo cargandolo ('file')
  uploded_file -> Informacion el csv cargado
  
  
  Returns
  ------------------
  None
  """
  if input == 'file':
    df_shares = pd.read_csv(uploded_file)
  elif input == 'template':
    url = 'https://github.com/napo178/prueba01/blob/main/analisis_comments_tiktok.csv'
    df_shares = pd.read_csv(url)
    
  texto_de_publicaciones = df_shares['ShareCommentary']
  texto_de_publicaciones = [i for i in texto_de_publicaciones if type(i) == str]

  # Uso set para borrar repetidos
  texto = [i for i in set(texto_de_publicaciones) if type(i) == str]

  texto = ''.join(texto)

  # Limpiamos
  clean_texto = limpiar_puntuacion_stopwords(texto)

  # Hacemos el wordcloud
  word_cloud = WordCloud(height=800, width=800, background_color='white',max_words=100, min_font_size=5).generate(clean_texto)
  fig, ax = plt.subplots()

  # Sacamos los ticks de los ejes 
  ax.axis('off')

  ax.imshow(word_cloud)
  title_alignment = """
  <style> #the-title { 
  text-align: center
  }
  </style>"""

  st.markdown(title_alignment, unsafe_allow_html=True)

  st.title("Nube de palabras")
  fig  # 👈 Draw a Matplotlib chart
  
  fig.savefig("nube.png")
  
  st.markdown('# Descargar la imagen')
  with open("nube.png", "rb") as file:
    btn = st.download_button(
      label="Guardar imagen",
      data=file,
      file_name="nube.png",
      mime="image/png"
    )

  st.markdown('''
  .linkedin.com/in/gustavo-juantorena/) y [Github](https://github.com/GEJ1)
  ''')

# Obtengo la lista de stopwords (conectores, preposiciones, etc) en espanol gracias a nltk
nltk.download('stopwords')
stop_words = stopwords.words('spanish')


if __name__ == "__main__": 

  st.title('☁️ Nube de palabras Tick Tock ☁️')
  st.markdown("Creado por Napoleón Pérez")

  st.markdown('## Presioná el botón **Browse files** y luego seleccioná tu archivo *comment_tiktok.csv*')      
  pressed = st.button('Ver ejemplo')

  # Cargamos template
  if pressed:
     generar_nube_de_palabras('template')
  
  # Subir archivo
  uploaded_file = st.file_uploader("Seleccioná el archivo")

  # Cargamos desde archivo
  if uploaded_file is not None:
    generar_nube_de_palabras('file', uploaded_file)