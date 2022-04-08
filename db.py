from mysql.connector import connect, Error
from secrets import get_secret

from requests import delete

DB_HOST = get_secret('db_host')
DB_USER = get_secret('db_user')
DB_PASSWORD = get_secret('db_password')
DB = "cinecolombia"
DB_TABLE_PLAYING = "playing"
DB_TABLE_UPCOMING = "upcoming"
MAX_AMOUNT = 50

def fetch(query, phrase=''):
    try:
        with connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
    except Error as e:
        print(e)
    finally:
        if phrase != '':
            print(phrase)

def execute(query, phrase=''):
    try:
        with connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
    except Error as e:
        print(e)
    finally:
        if phrase != '':
            print(phrase)

def execute_many(query, records, phrase=''):
    try:
        with connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB,
        ) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(query, records)
                connection.commit()
    except Error as e:
        print(e)
    finally:
        if phrase != '':
            print(phrase)

def get_all_records(table):
    query = f"SELECT date, title, year, genres, country, language, runtime, director, actors, rating, is_wanted, presale, poster, link, tmdb_id, imdb_id, title_slug, plot FROM {table}"
    records = fetch(query)
    return records

def delete_records(table):
    delete_movies = f"DELETE FROM {table}"
    execute(delete_movies)
    print(f"[MySQL] Deleting all records from table '{table}'")

def is_in_records(tmdb_id, table):
    records = get_all_records(table)
    for record in records:
        record_tmdb = record[14]
        if record_tmdb != tmdb_id:
            continue
        else:
            return True
    else:
        return False

def add_records(list, table):
    date = list.date
    title = list.title
    year = list.omdb.year
    genres = ", ".join(list.genres)
    country = list.omdb.country
    language = list.omdb.language
    runtime = list.omdb.runtime
    director = list.omdb.director
    actors = list.omdb.actors
    rating = list.tmdb.rating
    is_wanted = list.is_wanted
    presale = list.presale
    poster = list.omdb.poster
    link = list.link
    tmdb_id = list.tmdb.tmdb_id
    imdb_id = list.omdb.imdb_id.split('/')[-1]
    title_slug = list.tmdb.title_slug
    plot = list.tmdb.plot

    movie_query = f"""
    INSERT INTO {table}
    (date, title, year, genres, country, language, runtime, director, actors, rating, is_wanted, presale, poster, link, tmdb_id, imdb_id, title_slug, plot)
    VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"""

    records = [
        date,
        title,
        year,
        genres,
        country,
        language,
        runtime,
        director,
        actors,
        rating,
        is_wanted,
        presale,
        poster,
        link,
        tmdb_id,
        imdb_id,
        title_slug,
        plot,
        ],

    phrase = f"[MySQL] Movie added: {title}"
    
    execute_many(movie_query, records, phrase)

