from mysql.connector import connect, Error
from secrets import json_secret

DB_HOST = json_secret('db', 'host')
DB_USER = json_secret('db', 'user')
DB_PASSWORD = json_secret('db', 'password')
DB = json_secret('db', 'db')
MAX_AMOUNT = 50

try:
    with connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB,
    ) as connection:

        create_cinecolombia_playing_table_query = """
        CREATE TABLE playing(
            id INT AUTO_INCREMENT PRIMARY KEY,
            date VARCHAR(20),
            title VARCHAR(150),
            year INT(4),
            genres VARCHAR(100),
            country VARCHAR(50),
            language VARCHAR(50),
            runtime VARCHAR(10),
            director VARCHAR(100),
            actors VARCHAR(300),
            rating VARCHAR(5),
            is_wanted TINYINT(1),
            presale TINYINT(1),
            poster VARCHAR(300),
            link VARCHAR(300),
            tmdb_id VARCHAR(20),
            imdb_id VARCHAR(20),
            title_slug VARCHAR(100),
            plot VARCHAR(700)
        )
        """
        create_cinecolombia_upcoming_table_query = """
        CREATE TABLE upcoming(
            id INT AUTO_INCREMENT PRIMARY KEY,
            date VARCHAR(20),
            title VARCHAR(150),
            year INT(4),
            genres VARCHAR(100),
            country VARCHAR(50),
            language VARCHAR(50),
            runtime VARCHAR(10),
            director VARCHAR(100),
            actors VARCHAR(300),
            rating VARCHAR(5),
            is_wanted TINYINT(1),
            presale TINYINT(1),
            poster VARCHAR(300),
            link VARCHAR(300),
            tmdb_id VARCHAR(20),
            imdb_id VARCHAR(20),
            title_slug VARCHAR(100),
            plot VARCHAR(700)
        )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_cinecolombia_playing_table_query)
            cursor.execute(create_cinecolombia_upcoming_table_query)
            connection.commit()

        print('Tables created.\n')
    

except Error as e:
    print(e)

