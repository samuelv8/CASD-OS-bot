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
    print(f"ESTA EH A TABELA {tb}")
    select = "SELECT * FROM " + tb
    cursor = connect.cursor()
    cursor.execute(select)
    result = cursor.fetchall()
    for linha in result:
        print(linha)
    print()


def save_name(info: str, id: int, connect):
    cursor = connect.cursor()
    records = "INSERT INTO ordens (id_cellphone, nome, status) VALUES (?, ?, ?)"
    cursor.execute(records, (id, info, 2))
    connect.commit()
    # show_table('ordens', connect)


def save_ap(info: str, id: int, connect):
    records = "UPDATE ordens SET ap=? WHERE status = 2"
    cursor = connect.cursor()
    cursor.execute(records, (info,))
    connect.commit()
    # show_table('ordens', connect)


def save_proom(info: str, id: int, connect):
    records = "UPDATE ordens SET p_room=? WHERE status = 2"
    cursor = connect.cursor()
    cursor.execute(records, (info,))
    connect.commit()
    # show_table('ordens', connect)


def save_ptype(info: str, id: int, connect):
    records = "UPDATE ordens SET p_type=? WHERE status = 2"
    cursor = connect.cursor()
    cursor.execute(records, (info,))
    connect.commit()
    # show_table('ordens', connect)


def save_pdescription(info: str, id: int, connect):
    records = "UPDATE ordens SET p_description=? WHERE status = 2"
    records2 = "UPDATE ordens SET status=? WHERE status = 2"
    cursor = connect.cursor()
    cursor.execute(records, (info,))
    cursor.execute(records2, (0,))
    connect.commit()
    # show_table('ordens', connect)


def save_synonym(given_info: str, intended_info: str, yes: bool, connect):
    # a conexão desse banco deve ser feita em Voce quis dizer para combar com aprendizado de maquina
    records = "INSERT INTO sinonimos (intended, given, status) VALUES (?, ?, ?)"
    cursor = connect.cursor()
    cursor.execute(records, (intended_info, given_info, yes))
    connect.commit()
    # show_table('sinonimos', connect)

def search_order(id, connect):
    temp = """SELECT id_cellphone, p_description FROM ordens WHERE status = 0"""
    cursor = connect.cursor()
    cursor.execute(temp)
    n = cursor.fetchall()
    if n:
        index = 1
        posicoes = []
        for v in n:
            posicoes.append((v, index))
            index = index + 1
        busca_final = []
        for v in posicoes:
            if v[0][0] == int(id):
                busca_final.append((v[0][1], v[1]))
        return busca_final
    return -1



if __name__ == '__main__':
    pass
