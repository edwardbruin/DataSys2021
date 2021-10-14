import mysql.connector

_host = "192.168.1.6",
_user = "remoteuser",
_password = "password",
_database = "datasys"


def main(argument, commit=False):
    mydb = mysql.connector.connect(
        host=_host,
        user=_user,
        password=_password,
        database=_password
    )

    mycursor = mydb.cursor()

    mycursor.execute(argument)

    myresult = mycursor.fetchall()
    if commit:
        mydb.commit()
    return myresult
