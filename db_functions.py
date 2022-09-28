from functions import db_auth

cursor, mydb = db_auth()

def UpdateSetWhere(table, column, where):

    sql = 'UPDATE %s SET %s WHERE %s' # fix
