"""
Module for executing SQL queries using psycopg2.

This module defines the `execute_sql` function, which allows executing SQL queries
using the psycopg2 library to interact with a PostgreSQL database.

"""

from psycopg2 import connect, OperationalError
from psycopg2.extras import RealDictCursor

USER = "postgres"
HOST = "localhost"
PASSWORD = "coderslab"


def execute_sql(sql_code, db, list_of_dictionaries=False):
    """
    Execute the given SQL code using psycopg2.

    Args:
        sql_code (str): The SQL code to execute.
        db (str): The name of the database to connect to.
        list_of_dictionaries (bool, optional): Whether to return the result as a list of dictionaries.
                                               Defaults to False.

    Returns:
        list: The data from the psycopg2 cursor as a list (can be None if nothing to fetch).

    Raises:
        OperationalError: If there is an error during the database connection.
    """

    try:
        # Attempt to establish a connection to the database
        connection = connect(user=USER, password=PASSWORD, host=HOST, database=db)
    except OperationalError as error:
        # If there's an error, print the message and return None
        print(f'Error connecting to the database:\n{error}')
        return None

    # Set autocommit to True to make changes permanent
    connection.autocommit = True

    if list_of_dictionaries:
        # Change the response type from a list of tuples to a list of dictionaries
        cursor = connection.cursor(cursor_factory=RealDictCursor)
    else:
        cursor = connection.cursor()

    results = None  # Default response of the function

    cursor.execute(sql_code)

    if 'select' in sql_code.lower():
        # If the SQL code is a SELECT query, override the results variable with a list of rows
        results = [row for row in cursor]

    # Close the cursor and the connection
    cursor.close()
    connection.close()

    return results


if __name__ == '__main__':
    # Example usage
    result = execute_sql('SELECT * FROM Book', 'library_db')
    print(result)

    dict_result = execute_sql('SELECT * FROM Book', 'library_db', True)
    print(dict_result)

    result2 = execute_sql('SELECT * FROM client', 'library_db')
    print(result2)

    dict_result2 = execute_sql('SELECT * FROM client', 'library_db', True)
    print(dict_result2)