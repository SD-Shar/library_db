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
    
    
    
@app.route('/')
def index():
    return redirect('/signup')
    
    
# SIGN UP FO RNEW ACCOUNT:
@app.route('/signup', methods=["GET", "POST"])
def signup():
    
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

    return render_template("signup.html")






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
        
        if brukere and check_password_hash(brukere['passord_hash'], passord):
        # if brukere and brukere['passord_hash'] == passord:
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
    
    if "epost" not in session:
        return redirect(url_for("login"))
    
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM boker")
    boker = mycursor.fetchall() #liste??

    return render_template("browse_kunde.html", boker=boker, epost=session['epost'])



# BORROW BOOKS
@app.route('/login/browse_kunde/borrowed_kunde', methods=["GET", "POST"])
def borrowed_kunde():
    
    if "bruker_id" not in session:
        return redirect(url_for("login"))
    
    bruker_id = session["bruker_id"]
    
    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute("""SELECT b.bok_navn, b.bok_forfatter, be.tid_av_bestilling
                     FROM bestilling be
                     JOIN boker b ON be.bok_id = b.id WHERE be.bruker_id = %s ORDER BY be.tid_av_bestilling DESC""", (bruker_id,))
    borrowed_books = mycursor.fetchall()
    
    
    return render_template("borrowed_kunde.html", borrowed_books=borrowed_books)





# BESTILLING
@app.route('/login/browse_kunde/borrow/<int:bok_id>')
def borrow_book(bok_id):
    
    bruker_id = session['bruker_id']
    
    mydb = get_connection()
    mycursor = mydb.cursor()
    
    mycursor.execute("INSERT INTO bestilling (bruker_id, bok_id) VALUES (%s, %s)", (bruker_id, bok_id)
    )
    mydb.commit()
        
    return redirect(url_for("borrowed_kunde"))



# !LIBRARIAN!

# LIBRARIAN HOME PAGE
@app.route('/login/homepage_lib')
def homepage_lib():
    if session.get("rolle") == "admin":
        
        mydb = get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM boker")
        boker = mycursor.fetchall() #liste??
        return render_template("homepage_lib.html", epost=session['epost'], boker=boker)
        



# OVERVIEW OF CUSTOMERS AND WHAT THEY'VE BORROWED (for librarian)
@app.route('/login/homepage_lib/overview_lib')
def overview_lib():
    if session.get("rolle") == "admin":
        mydb = get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM bestilling")
        bestilling = mycursor.fetchall() #liste??
    
    return render_template('overview_lib.html', bestilling=bestilling)



# ADD NEW BOOKS (for librarian)
@app.route("/login/homepage_lib/add_books_lib", methods=["GET", "POST"])
def add_books_lib():
    
    if session.get("rolle") == "admin":
        if request.method == "POST":
            
            name = request.form["bok_navn"]
            author = request.form["bok_forfatter"]
            
            mydb = get_connection()
            mycursor = mydb.cursor()
            
            mycursor.execute("INSERT INTO boker (bok_navn, bok_forfatter) VALUES (%s, %s)", (name, author))
            mydb.commit()
            mycursor.close()
            mydb.close()
            
            return redirect("/login/homepage_lib")
    return render_template('add_books_lib.html', )






if __name__ == '__main__':
    app.run(debug=True)
    