from etl import extract_and_transform_recently_played_data, load_data_to_database
from config.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth
import spotipy
from datetime import timedelta, datetime
from visualizations import generate_top_artists_bar_chart,generate_word_cloud

# Configuración de autenticación con Spotipy
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
                              scope="user-read-recently-played"))

if __name__ == "__main__":
    # Obtener marca de tiempo UNIX para obtener datos desde ayer
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Extraer y transformar los datos recientes de reproducción
    recently_played_data = extract_and_transform_recently_played_data(sp, yesterday_unix_timestamp)

    # Cargar los datos en la base de datos
    load_data_to_database(recently_played_data)

    # Visualizaciones
    generate_word_cloud(recently_played_data)
    generate_top_artists_bar_chart(recently_played_data)