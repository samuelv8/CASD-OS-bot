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

records = "INSERT INTO db_service_orders (id_cellphone, nome, ap, p_room, p_type, p_description, status) VALUES (51999207247, 'Alexandre bernat', '315 b', 'cozinha', 'vazamento', 'pia fudida', 0)"
execute_query(connection, records)

select = "SELECT * FROM db_service_orders"
lida = execute_read_query(connection, select)

for linha in lida:
    print(linha)

def save_information(info: str, type: str, id: int):
    pass


def save_synonym(given_info: str, intended_info: list, yes: bool):
    pass
