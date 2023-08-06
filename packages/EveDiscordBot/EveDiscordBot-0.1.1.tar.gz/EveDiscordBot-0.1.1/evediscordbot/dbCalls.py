import mysql.connector
import datetime
import os
host_var = os.environ['host_var']
username_var = os.environ['username_var']
pass_var = os.environ['pass_var']
def opendb():
    '''Helper function that opens database connection'''

    return mysql.connector.connect(host=host_var, user=username_var,
                                   password=pass_var)


def enterStrike(userID,username):
    '''enters a strike for the specified user'''
    mydb = opendb()
    time = datetime.datetime.now()
    print(time)
    cursor = mydb.cursor()
    sql = "INSERT INTO evelynnmains.striketable(userid,strikeDate,username) VALUES (%s,%s,%s) "
    inserttuple = (userID,time,username)
    cursor.execute(sql,inserttuple)
    mydb.commit()
    print("done")
    mydb.close()


def clearStrikes(userID):
    '''clears ALL strikes for the specified user'''
    mydb = opendb()
    cursor = mydb.cursor()
    sql = "DELETE FROM  evelynnmains.striketable WHERE userid = %s"
    user = (userID,)
    cursor.execute(sql,user)
    mydb.commit()
    mydb.close()



def getallStrikes():
    ''' returns strikes for all users in the database as a markdown formatted string'''
    mydb = opendb()
    cursor = mydb.cursor()
    sql = "SELECT username,COUNT(userid),MAX(strikeDate) FROM evelynnmains.striketable GROUP BY userid ORDER  BY COUNT(userid) ASC "
    cursor.execute(sql)

    result = cursor.fetchall()

    outstr = '| Username                       | Strikes | Latest Strike (CST) |\n|--------------------------------|---------|---------------------|'

    for i in result:
        y = 31 - len(i[0])
        namespace = " " * y
        outstr = outstr + (('\n| {}| {}       | {} |').format(i[0] + namespace, i[1], i[2]))
    mydb.close()
    return outstr

def getStrikes(userID):
    mydb = opendb()
    cursor = mydb.cursor()
    sql = "SELECT COUNT(userid) FROM evelynnmains.striketable WHERE userid= %s"
    user = (userID,)
    cursor.execute(sql,user)
    result = cursor.fetchall()
    return result[0][0]
    mydb.commit()
    mydb.close()



