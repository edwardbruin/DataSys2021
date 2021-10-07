import mysql.connector


def main(argument, commit=False):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="shippingcompany"
    )

    mycursor = mydb.cursor()

    mycursor.execute(argument)

    myresult = mycursor.fetchall()
    if commit:
        mydb.commit()
    return myresult
