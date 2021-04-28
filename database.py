import sqlite3


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

conn = sqlite3.connect("tasks.db")

cursor = conn.cursor()

cursor.execute("""DROP TABLE tasks""")

create_tasks_query = """CREATE TABLE tasks (
    id integer PRIMARY KEY,
    tanggal date NOT NULL,
    matkul text NOT NULL,
    tugas text NOT NULL,
    topik text NOT NULL
);"""
cursor.execute(create_tasks_query)