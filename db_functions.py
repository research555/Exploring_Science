from functions import DbAuth

cursor, mydb = DbAuth()
def SetSuccess(success: int, university):
    sql = 'UPDATE universities SET success = %s WHERE institution = %s'
    cursor.execute(sql, (success, university,))
    mydb.commit()
def SetTried(tried: int, university):
    sql = 'UPDATE universities SET tried = %s WHERE institution = %s'
    cursor.execute(sql, (tried, university,))
    mydb.commit()
