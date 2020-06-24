import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connect, query):
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        connect.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connect, query):
    cursor = connect.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def show_table(tb, connect):
    select = "SELECT * FROM ordens"
    cursor = connect.cursor()
    cursor.execute(select)
    result = cursor.fetchall()
    for linha in result:
        print(linha)


def save_name(info: str, id: int, connect):
    cursor = connect.cursor()
    try:
        records = "INSERT INTO ordens (id_cellphone, nome) VALUES (?, ?)"
        cursor.execute(records, (id, info))
    except:
        records = "UPDATE ordens SET nome=? WHERE id_cellphone=?"
        cursor = connect.cursor()
        cursor.execute(records, (info, id))

    connect.commit()
    show_table('ordens', connect)


def save_ap(info: str, id: int, connect):
    records = "UPDATE ordens SET ap=? WHERE id_cellphone=?"
    cursor = connect.cursor()
    cursor.execute(records, (info, id))
    connect.commit()
    show_table('ordens', connect)


def save_proom(info: str, id: int, connect):
    records = "UPDATE ordens SET p_room=? WHERE id_cellphone=?"
    cursor = connect.cursor()
    cursor.execute(records, (info, id))
    connect.commit()
    show_table('ordens', connect)


def save_ptype(info: str, id: int, connect):
    records = "UPDATE ordens SET p_type=? WHERE id_cellphone=?"
    cursor = connect.cursor()
    cursor.execute(records, (info, id))
    connect.commit()
    show_table('ordens', connect)


def save_pdescription(info: str, id: int, connect):
    records = "UPDATE ordens SET p_description=? WHERE id_cellphone=?"
    cursor = connect.cursor()
    cursor.execute(records, (info, id))
    connect.commit()
    show_table('ordens', connect)


def save_synonym(given_info: str, intended_info: str, yes: bool, connect):
    # a conexão desse banco deve ser feita em Voce quis dizer para combar com aprendizado de maquina
    records = "INSERT INTO db_synonyms (intended, given, status) VALUES (intended_info, given_info, yes)"
    execute_query(connect, records)


if __name__ == '__main__':

    connection = create_connection('C:\\Users\\alexa\\bot-da-os\\db_orders.db')
    create_os_table = """
    CREATE TABLE IF NOT EXISTS ordens (
    
      id_cellphone INTEGER PRIMARY KEY,
      nome TEXT NOT NULL,
      ap TEXT,
      p_room TEXT,
      p_type TEXT,
      p_description TEXT
      
    );"""

    execute_query(connection, create_os_table)

    create_os_synonyms = """
    CREATE TABLE IF NOT EXISTS sinonyms (
      id IDENTITY 
      intended TXT NOT NULL PRIMARY KEY,
      given TXT NOT NULL,
      status BIT NOT NULL
    );"""
    # execute_query(connection, create_os_synonyms)

    #deletar = "DROP TABLE ordens"
    #connection.cursor().execute(deletar)

    show_table('his', connection)

    connection.close()
