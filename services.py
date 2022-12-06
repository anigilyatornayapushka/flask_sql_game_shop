from typing import Any
import datetime
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import (
    connection as Connection,
    cursor as Cursor
)

from config import (
    HOST,
    PASSWORD,
    PORT,
    USER,
)


class Connection:
    """Class for working to DataBase"""

    def get_time(self) -> datetime.datetime:
        return datetime.datetime.now()

    def __init__(self) -> None:
        try:
            self.connection: Connection = psycopg2.connect(
                user=USER,
                host=HOST,
                port=PORT,
                password=PASSWORD,
                dbname="online_game_shop"
            )
            print(f"{self.get_time()} [INFO] Connection is successful")
        except (Exception, Error) as e:
            print("{0} [ERROR] Connection to database is bad: {1}".format(
                datetime.datetime.now(),
                e
            ))

    def __new__(cls: type[Any]) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls)

        return cls.instance

    def create_tables(self) -> None:
        with self.connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users(
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL
                );
                
                CREATE TABLE IF NOT EXISTS genres(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(50) UNIQUE NOT NULL,
                    description TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS games(
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(50) UNIQUE NOT NULL,
                    description TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    genre_id INTEGER REFERENCES genres(id)
                );
            """)
        self.connection.commit()
        print(f"{self.get_time()} [INFO] Tables is created")

    def get_users(self) -> list[tuple]:
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute('SELECT * FROM users;')
            data = cur.fetchall()
        self.connection.commit()
        return data

    def create_user(self, login: str, password: str) -> None:
        if self.get_users() == []:
            with self.connection.cursor() as cur:
                cur.execute(f'''
                    INSERT INTO users (login, password)
                    VALUES ('{login}', '{password}');
                ''')
        self.connection.commit()

    def get_genres(self) -> list[tuple]:
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute('SELECT * FROM genres')
            data = cur.fetchall()
        return data

    def create_genre(self, title: str, description: str) -> None:
        try:
            genre_id: int = 1 + len(self.get_genres())
            with self.connection.cursor() as cur:
                cur.execute(f'''
                    INSERT INTO genres (id, title, description)
                    VALUES ({genre_id}, '{title}', '{description}')
                ''')
        except: ...
        self.connection.commit()

    def get_games(self) -> list[tuple]:
        data: list[tuple] = []
        with self.connection.cursor() as cur:
            cur.execute('SELECT * FROM games')
            data = cur.fetchall()
        return data

    def create_game(self, title: str, description: str, rating: int, genre_id: int) -> None:
        game_id: int = 1 + len(self.get_games())
        try:
            with self.connection.cursor() as cur:
                cur.execute(f'''
                    INSERT INTO games (id, title, description, rating, genre_id)
                    VALUES ({game_id}, '{title}', '{description}', '{rating}', '{genre_id}')
                ''')
        except: ...
        self.connection.commit()

    def close_connection(self) -> None:
        self.connection.close()
        print(f'{datetime.datetime.now()} [INFO] Connection is close')