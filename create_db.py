import mysql.connector

try:

    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password = 'write your password'
    )
    sor = mydb.cursor()

    # sor.execute("CREATE DATABASE our_users")

    sor.execute("SHOW DATABASES")

    for db in sor:
        print(db)

except Exception as err:
    print("error",err) 

