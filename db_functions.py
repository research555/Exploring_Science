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


def SetSuccess(success: int, university):
    sql = 'UPDATE universities SET success = %s WHERE institution = %s'
    cursor.execute(sql, (success, university,))
    mydb.commit()
def SetTried(tried: int, university):
    sql = 'UPDATE universities SET tried = %s WHERE institution = %s'
    cursor.execute(sql, (tried, university,))
    mydb.commit()
