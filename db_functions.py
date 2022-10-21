from dotenv import load_dotenv
import os
import mysql.connector

def DbAuth():
    # init database

    load_dotenv()

    # # # # Define auth details # # # #

    DB_HOSTNAME = os.getenv('DB_HOSTNAME')
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_DATABASE = os.getenv('DB_DATABASE')

    # # # # Connect to MySQL Database# # # #

    mydb = mysql.connector.connect(
        host=DB_HOSTNAME,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

    cursor = mydb.cursor(buffered=True)  # Name the cursor something simple for easier use

    return cursor, mydb

cursor, mydb = DbAuth()


def ReorganizeSQL(CREATE, LIKE, LIMIT, amount_tables):
    for table_number in range(1, amount_tables + 1):
        sql = f'CREATE TABLE {CREATE}{table_number} LIKE {LIKE}'
        cursor.execute(sql)  # makes new tables
        mydb.commit()
        sql = f'INSERT INTO {CREATE}{table_number} SELECT * FROM {LIKE} LIMIT {LIMIT}'
        cursor.execute(sql)  # inserts 50k into new table
        mydb.commit()
        sql = f'DELETE FROM {LIKE} LIMIT 50000'
        cursor.execute(sql)
        mydb.commit()


def SetSuccess(success: int, university):
    sql = 'UPDATE universities SET success = %s WHERE institution = %s'
    cursor.execute(sql, (success, university,))
    mydb.commit()

def SetTried(tried: int, university):
    sql = 'UPDATE universities SET tried = %s WHERE institution = %s'
    cursor.execute(sql, (tried, university,))
    mydb.commit()
