import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("db_orders.db")


def execute_query(connect, query):
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        connect.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


create_os_table = """
CREATE TABLE IF NOT EXISTS db_service_orders (
  os_position INTEGER IDENTITY, 
  id_cellphone INTEGER PRIMARY KEY,
  nome TEXT NOT NULL,
  ap TEXT,
  p_room TEXT,
  p_type TEXT,
  p_description TEXT,
  status BIT NOT NULL
);"""
execute_query(connection, create_os_table)

create_os_synonyms = """
CREATE TABLE IF NOT EXISTS db_synonyms (
  id IDENTITY 
  intended TXT NOT NULL PRIMARY KEY,
  given TXT NOT NULL,
  status BIT NOT NULL
);"""

def save_information(info: str, nome_da_col: str, id: int):
    records = "INSERT INTO db_service_orders (id_cellphone, nome_da_col) VALUES (id, info)"
    execute_query(connection, records)


def save_synonym(given_info: str, intended_info: str, yes: bool):
    records = "INSERT INTO db_synonyms (intended, given, status) VALUES (intended_info, given_info, yes)"
    execute_query(connection, records)

def show_table (tb):
    select = "SELECT * FROM tb"
    lida = execute_read_query(connection, select)
    for linha in lida:
        print(linha)