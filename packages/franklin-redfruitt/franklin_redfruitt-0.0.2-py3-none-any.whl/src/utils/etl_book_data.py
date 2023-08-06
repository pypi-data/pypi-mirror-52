import csv
import psycopg2

connection = None


def create_conn_obj():
    """ Factory method to return connection obj.
    """
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="sa@123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="bookrecommendations")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    return connection


def create_table(query):
    """ Wrapper method for creating table in postgres.
    """
    try:
        connection = create_conn_obj()

        cursor = connection.cursor()
        cursor.execute(query)

        connection.commit()

        print("Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def insert_into_table(query, records):
    """ Wrapper method for creating table in postgres.
    """
    try:
        connection = create_conn_obj()

        cursor = connection.cursor()
        cursor.executemany(query, records)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into table")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def load_bx_users_dataset(dataset_path):
    """ Pipeline for loading bx users dataset.
    """
    with open(dataset_path) as f:
        # Extract
        raw_data = csv.reader(f, delimiter=';')
        next(raw_data, None)
        # Transform
        transformed_result = []

        for data in raw_data:
            if data[2] == 'NULL':
                data[2] = None
            else:
                data[2] = float(data[2])
            insert_set = (data[0], data[1], data[2])
            transformed_result.append(insert_set)

        # Load
        query = '''CREATE TABLE IF NOT EXISTS bx_users
                (id serial PRIMARY KEY     NOT NULL,
                user_id           TEXT    NOT NULL,
                location          TEXT    NOT NULL,
                age         INT); '''
        create_table(query)

        insert_query = '''
                       INSERT INTO bx_users (user_id, location, age)
                               VALUES (%s,%s,%s)
                       '''
        insert_into_table(insert_query, transformed_result)


def load_bx_ratings_dataset(dataset_path):
    """ Pipeline for loading bx users dataset.
    """
    with open(dataset_path) as f:
        # Extract
        raw_data = csv.reader(f, delimiter=';')
        next(raw_data, None)
        # Transform
        transformed_result = []

        for data in raw_data:
            if data[2] == 'NULL':
                data[2] = None
            else:
                data[2] = float(data[2])
            insert_set = (data[0], data[1], data[2])
            transformed_result.append(insert_set)

        # Load
        query = '''CREATE TABLE IF NOT EXISTS bx_ratings
                (id serial PRIMARY KEY     NOT NULL,
                user_id           TEXT    NOT NULL,
                isbn          TEXT    NOT NULL,
                book_rating         INT); '''
        create_table(query)

        insert_query = '''
                       INSERT INTO bx_ratings (user_id, isbn, book_rating)
                               VALUES (%s,%s,%s)
                       '''
        insert_into_table(insert_query, transformed_result)


def load_bx_books_dataset(dataset_path):
    """ Pipeline for loading bx books dataset.
    """
    with open(dataset_path) as f:
        # Extract
        raw_data = csv.reader(f, delimiter=';')
        next(raw_data, None)
        # Transform
        transformed_result = []

        for data in raw_data:
            # if data[2] == 'NULL':
            #     data[2] = None
            # else:
            #     data[2] = float(data[2])
            insert_set = (data[0], data[1], data[2], data[3])
            transformed_result.append(insert_set)

        # Load
        query = '''CREATE TABLE IF NOT EXISTS bx_books
                (id serial PRIMARY KEY     NOT NULL,
                isbn                TEXT    NOT NULL,
                book_title          TEXT    NOT NULL,
                book_author         TEXT    NOT NULL,
                year_of_publication TEXT    NOT NULL
                ); '''
        create_table(query)

        insert_query = '''
                       INSERT INTO bx_books (isbn, book_title, book_author,
                        year_of_publication)
                               VALUES (%s,%s,%s,%s)
                       '''
        insert_into_table(insert_query, transformed_result)


if __name__ == '__main__':
    # users_dataset_path = 'D:\Code\Python\BookRecommendation\data
    # \BX-Users.csv'
    # load_bx_users_dataset(users_dataset_path)

    # books_dataset_path = 'D:\Code\Python\BookRecommendation\data
    # \BX-Books.csv'
    # load_bx_books_dataset(books_dataset_path)

    r_path = 'D:\Code\Python\BookRecommendation\data\BX-Book-Ratings.csv'
    load_bx_ratings_dataset(r_path)
