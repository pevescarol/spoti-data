from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

def generate_word_cloud(df):
    # Concatenar los nombres de las canciones en una sola cadena
    text = ' '.join(df['song_name'].astype(str).tolist())

    # Crear el Word Cloud
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110, background_color='white').generate(text)

    # Visualizar el Word Cloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.title('Word Cloud de Nombres de Canciones')
    plt.show()


#Proporciona una representación visual de las palabras más frecuentes en los nombres de las canciones escuchadas durante hoy y ayer



def generate_top_artists_bar_chart(df):
    # Calcular la cuenta de reproducciones por artista
    artist_counts = df['artist_name'].value_counts().reset_index()
    artist_counts.columns = ['artist_name', 'count']

    # Visualizar el gráfico de barras
    plt.figure(figsize=(12, 6))
    sns.barplot(x='artist_name', y='count', data=artist_counts.head(10))
    plt.title('Top 10 Artistas Reproducidos Recientemente')
    plt.xlabel('Artista')
    plt.ylabel('Número de Reproducciones')
    plt.xticks(rotation=45, ha='right')

    # Forzar la presentación de valores enteros en el eje Y
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.show()

#Destaca los artistas más frecuentes en el historial de reproducción durante hoy y ayer.