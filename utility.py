import json
import sqlite3
from sqlite3 import Error

import discord


def write_json(new_data, filename):
    with open(filename, 'r') as file:
        file_data = json.load(file)
        file_data.update(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)


def create_connection(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def join_group(conn, GroupName, user):
        
    cur = conn.cursor()
    print ("before sql")
    sql = "INSERT INTO " + GroupName + " VALUES " + "("+ user +")"
    print("after sql")
    print(sql)
    cur.execute(sql)
    print ("its working")
    conn.commit()
    for row in cur.execute('SELECT * FROM test2 ORDER BY name'):
        print(row)
    return cur.lastrowid
