from flask import Flask, render_template, request, redirect
import mysql.connector
app = Flask(__name__)


def get_connection():
    return mysql.connector.connect(
        host="10.200.14.11",
        user="absolute_solver",
        password="silly",
        database="library_db"
    )


@app.route('/')
def kunder():
    
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM kunder")
    kunder = mycursor.fetchall() #liste??
    
    
    return render_template('index.html', kunder=kunder)



@app.route('/')
def boker():
    
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM boker")
    boker = mycursor.fetchall() #liste??
    
    
    return render_template('index.html', boker=boker)



@app.route('/borrow')
def bestilling():
    
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bestilling")
    bestilling = mycursor.fetchall() #liste??
    
    
    return render_template('index.html', bestilling=bestilling)






if __name__ == '__main__':
    app.run(debug=True)
    
