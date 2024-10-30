# db_connection.py

import mysql.connector
import pandas as pd
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="RootUser1234!",
            database="OnlineGrocer"
        )
        return connection
    except Error as e:
        print(f"Error: '{e}'")
        return None

# Execute read queries
def execute_read_query(query, params=None):
    try:
        connection = create_connection()
        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return pd.DataFrame(result)
    except Error as e:
        print(f"Error: '{e}'")
        return None

# Execute write (insert, update, delete) queries
def execute_write_query(query, params):
    try:
        connection = create_connection()
        if connection is None:
            return False

        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
        connection.close()
        return True  # Return True to indicate success
    except Error as e:
        print(f"Error: '{e}'")
        return False  # Return False to indicate failure

# Check if database connection is working
def test_connection():
    try:
        connection = create_connection()
        if connection is not None:
            connection.close()
            return True
        else:
            return False
    except Error as e:
        print(f"Error: '{e}'")
        return False
