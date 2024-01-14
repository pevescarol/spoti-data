import pandas as pd
from datetime import datetime, timedelta
from config.config import DATABASE_LOCATION
import sqlalchemy
import sqlite3

def check_if_valid_data(df: pd.DataFrame) -> bool:
    """
    Verifica si los datos son válidos.

    Args:
        df (pd.DataFrame): DataFrame con los datos.

    Returns:
        bool: True si los datos son válidos, False de lo contrario.
    """
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    if df.isnull().values.any():
        raise Exception("Null values found")

    start_of_yesterday = datetime.now() - timedelta(days=1)
    start_of_yesterday = start_of_yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for timestamp in df['timestamp']:
        timestamp_date = datetime.strptime(timestamp, '%Y-%m-%d')
        if start_of_yesterday <= timestamp_date < start_of_today:
            pass
        else:
            print(f"At least one song does not have a timestamp corresponding to yesterday: {timestamp}")

    return True

def extract_and_transform_recently_played_data(sp, yesterday_unix_timestamp):
    """
    Extrae y transforma los datos recientes de reproducción de Spotify.

    Args:
        sp: Instancia de la clase Spotify con autenticación.
        yesterday_unix_timestamp: Marca de tiempo UNIX para obtener datos desde ayer.

    Returns:
        pd.DataFrame: DataFrame con los datos extraídos y transformados.
    """

    recently_played_spotipy = sp.current_user_recently_played(after=yesterday_unix_timestamp)

    print("Recently Played Spotipy JSON:")
    print(recently_played_spotipy)

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in recently_played_spotipy["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps,
    }

    song_df = pd.DataFrame(song_dict, columns=["song_name", "artist_name", "played_at", "timestamp"])

    return song_df

def load_data_to_database(song_df):
    """
    Carga los datos en la base de datos SQLite.

    Args:
        song_df (pd.DataFrame): DataFrame con los datos a cargar.
    """
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print(song_df)

    if check_if_valid_data(song_df):
        print("Data valid, proceed to Load stage")

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Closed database successfully")
