from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"

DATABASE = "workshop"
TABLE_USER = """
            CREATE TABLE users
            (
            id serial PRIMARY KEY,
            username varchar(255),
            hashed_password varchar(80)
            );
            """
TABLE_MESSAGES = """
            CREATE TABLE messages
            (
            id serial PRIMARY KEY,
            from_id int REFERENCES users(id)
                ON DELETE CASCADE,
            to_id int REFERENCES users(id)
                ON DELETE CASCADE,
            text text,
            creation_date timestamp
            );
            """


def create_db(db):
    try:
        cnx = connect(
            user=USER,
            password=PASSWORD,
            host=HOST
        )
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute("CREATE DATABASE {};".format(db))
        print('Baza utworzona')
    except OperationalError:
        print('Błąd operacji')
    except DuplicateDatabase:
        print('Baza danych już istnieje')
    finally:
        cursor.close()
        cnx.close()


def execute_sql(sql_code, db):
    try:
        cnx = connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=db
        )
        cnx.autocommit = True
        cursor = cnx.cursor()
        cursor.execute(sql_code)
        print("Tabela utworzona")
    except OperationalError:
        print('Błąd operacji')
    except DuplicateTable:
        print('Tabela już stworzona')

    finally:
        cursor.close()
        cnx.close()


if __name__ == "__main__":
    create_db(DATABASE)
    execute_sql(TABLE_USER, DATABASE)
    execute_sql(TABLE_MESSAGES, DATABASE)