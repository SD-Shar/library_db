from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = "secretkey"


# GET CONNECTION FROM FLASK
def get_connection():
    return mysql.connector.connect(
        host="10.200.14.11",
        user="absolute_solver",
        password="silly",
        database="library_db"
    )
    
    
    
# SIGN UP FO RNEW ACCOUNT:
@app.route('/index', methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        fornavn = request.form['fornavn']
        etternavn = request.form['etternavn']
        epost = request.form['epost']
        telefonnummer = request.form['telefonnummer']
        passord = generate_password_hash(request.form['passord'])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO brukere (fornavn, etternavn, epost, telefonnummer, passord_hash, rolle) VALUES (%s, %s, %s, %s, %s, %s )", 
            (fornavn, etternavn, epost, telefonnummer, passord, 'bruker'))
        
        conn.commit()
        cursor.close()
        conn.close()
        flash("User registered", "success")
        return redirect(url_for("login"))

    return render_template("index.html")






# LOGIN
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        epost = request.form['epost']
        passord = request.form['passord']
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM brukere WHERE epost = %s", (epost,))
        brukere = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # if brukere and check_password_hash(brukere['passord_hash'], passord):
        if brukere and brukere['passord_hash'] == passord:
            session['bruker_id'] = brukere['id']
            session['epost'] = brukere['epost']
            session['rolle'] = brukere['rolle']
            
            print(brukere['rolle'])
            
            if brukere['rolle'] == 'admin':
                return redirect(url_for("homepage_lib"))
            else:
                return redirect(url_for("browse_kunde"))
        else:
            return render_template("login.html", feil_melding="Something's not right, try again")
        
    return render_template("login.html")
        



# !CUSTOMERS!

# BROWSE BOOKS - HOME PAGE
@app.route('/login/browse_kunde')
def browse_kunde():
    if session.get("rolle") == "bruker":

        mydb = get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM boker")
        boker = mycursor.fetchall() #liste??

        return render_template("browse_kunde.html", boker=boker, epost=session['epost'])



# BORROW BOOKS
@app.route('/login/browse_kunde/borrowed_kunde')
def borrowed_kunde():
    
    if "bruker_id" not in session:
        return redirect(url_for("login"))
    
    bruker_id = session["bruker_id"]
    
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bestilling WHERE bruker_id = %s", (bruker_id,))
    borrowed_books = mycursor.fetchall()
    
    return render_template("borrowed_kunde.html", borrowed_books=borrowed_books)







# !LIBRARIAN!

# LIBRARIAN HOME PAGE
@app.route('/login/homepage_lib')
def homepage_lib():
    if session.get("rolle") == "admin":
        return render_template("homepage_lib.html", epost=session['epost'])
    return redirect(url_for("login"))



# OVERVIEW OF CUSTOMERS AND WHAT THEY'VE BORROWED (for librarian)
@app.route('/login/homepage_lib/overview_lib')
def overview_lib():
    
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM bestilling")
    customer = mycursor.fetchall() #liste??
    
    return render_template('overview_lib.html', customer=customer)



# ADD NEW BOOKS (for librarian)
@app.route("/login/homepage_lib/add_books_lib", methods=["GET", "POST"])
def add_books_lib():
    
    if request.method == "POST":
        
        name = request.form["bok_navn"]
        author = request.form["bok_forfatter"]
        
        mydb = get_connection()
        mycursor = mydb.cursor()
        
        mycursor.execute("INSERT INTO boker (bok_navn, forfatter) VALUES (%s, %s)", (name, author))
        mydb.commit()
        
        return redirect("/login/homepage_lib")
    return render_template('add_books.html', )









if __name__ == '__main__':
    app.run(debug=True)
    