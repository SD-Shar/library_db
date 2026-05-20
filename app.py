from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import date, timedelta

app = Flask(__name__)
app.secret_key = "secretkey"


# GET CONNECTION FROM FLASK
def get_connection():
    return mysql.connector.connect(
        host="10.200.14.11",
        # host="localhost",
        user="absolute_solver",
        password="silly",
        database="library_db",
    )


@app.route("/")
def index():
    return redirect("/signup")


# SIGN UP FO RNEW ACCOUNT:
@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        fornavn = request.form["fornavn"]
        etternavn = request.form["etternavn"]
        epost = request.form["epost"]
        telefonnummer = request.form["telefonnummer"]
        passord = generate_password_hash(request.form["passord"])

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO brukere (fornavn, etternavn, epost, telefonnummer, passord_hash, rolle) VALUES (%s, %s, %s, %s, %s, %s )",
            (fornavn, etternavn, epost, telefonnummer, passord, "bruker"),
        )

        conn.commit()
        cursor.close()
        conn.close()
        flash("User registered", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        epost = request.form["epost"]
        passord = request.form["passord"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM brukere WHERE epost = %s", (epost,))
        brukere = cursor.fetchone()
        cursor.close()
        conn.close()

        if brukere and check_password_hash(brukere["passord_hash"], passord):
            # if brukere and brukere['passord_hash'] == passord:
            session["bruker_id"] = brukere["id"]
            session["epost"] = brukere["epost"]
            session["rolle"] = brukere["rolle"]

            print(brukere["rolle"])

            if brukere["rolle"] == "admin":
                return redirect(url_for("homepage_lib"))
            else:
                return redirect(url_for("browse_kunde"))
        else:
            return render_template(
                "login.html", feil_melding="Something's not right, try again"
            )

    return render_template("login.html")


# !CUSTOMERS!


# BROWSE BOOKS - HOME PAGE
@app.route("/login/browse_kunde")
def browse_kunde():

    if "epost" not in session:
        return redirect(url_for("login"))

    mydb = get_connection()
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM boker")
    # ![19/5/26] TRYING SMT NEW
    # mycursor.execute("SELECT * FROM boker WHERE antall_boker !=0")
    boker = mycursor.fetchall()  # liste??

    mycursor.close()
    mydb.close()

    return render_template("browse_kunde.html", boker=boker, epost=session["epost"])


# BORROW BOOKS
@app.route("/login/browse_kunde/borrowed_kunde", methods=["GET", "POST"])
def borrowed_kunde():

    if "bruker_id" not in session:
        return redirect(url_for("login"))

    bruker_id = session["bruker_id"]

    mydb = get_connection()
    mycursor = mydb.cursor()

    # (had to ask chatgpt for this part)
    mycursor.execute(
        """SELECT b.id, b.bok_navn, b.bok_forfatter, be.bok_id, be.tid_av_bestilling, be.leveringsfrist
                     FROM bestilling be
                     JOIN boker b ON be.bok_id = b.id WHERE be.bruker_id = %s ORDER BY be.tid_av_bestilling DESC""",
        (bruker_id,),
    )
    borrowed_books = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return render_template("borrowed_kunde.html", borrowed_books=borrowed_books)


# BESTILLING
@app.route("/login/browse_kunde/borrow/<int:bok_id>")
def borrow_book(bok_id):

    bruker_id = session["bruker_id"]

    mydb = get_connection()
    mycursor = mydb.cursor()

    # AI overview - original info fra "levelup.gitconnected.com"/"Medium"
    leveringsfrist = date.today() + timedelta(days=30)
    mycursor.execute(
        "INSERT INTO bestilling (bruker_id, bok_id, leveringsfrist) VALUES (%s, %s, %s)",
        (bruker_id, bok_id, leveringsfrist),
    )

    # ![15/3/26]
    mycursor.execute(
        "UPDATE boker SET antall_boker = antall_boker -1 WHERE id = %s", (bok_id,)
    )
    mydb.commit()

    mycursor.close()
    mydb.close()

    return redirect(url_for("borrowed_kunde"))


# TILBAKE LEVERING
@app.route("/login/browse_kunde/<int:bok_id>")
def return_book(bok_id):

    bruker_id = session["bruker_id"]

    mydb = get_connection()
    mycursor = mydb.cursor()

    # ![15/3/26]
    mycursor.execute(
        "DELETE FROM bestilling WHERE bruker_id = %s AND bok_id = %s LIMIT 1",
        (bruker_id, bok_id),
    )

    # ![15/3/26]
    mycursor.execute(
        "UPDATE boker SET antall_boker = antall_boker +1 WHERE id = %s", (bok_id,)
    )
    mydb.commit()

    mycursor.close()
    mydb.close()

    return redirect(url_for("borrowed_kunde"))


# ![13/5/26] FAQ SITE
@app.route("/faq_kunde", methods=["GET", "POST"])
def faq_kunde():

    if "epost" not in session:
        return redirect(url_for("login"))

    mydb = get_connection()
    mycursor = mydb.cursor()

    # NEW QUESTION
    if request.method == "POST":

        new_q = request.form["new_q"]
        bruker_id = session["bruker_id"]

        mycursor.execute(
            "INSERT INTO ny_faq (bruker_id, sporsmal) VALUES (%s, %s)",
            (bruker_id, new_q),
        )
        mydb.commit()

    # SPØRSMÅL - pre-done og nye:

    # INITIAL QUESTIONS
    mycursor.execute("SELECT * FROM ny_faq WHERE bruker_id = 1")
    init_q = mycursor.fetchall()

    # NYE SPØRSMÅL
    # mycursor.execute("SELECT * FROM ny_faq WHERE bruker_id != 1")
    # ny_q = mycursor.fetchall()
    
    # ![19/5/26] - NEW personal qquestions
    bruker_id = session[bruker_id]
    mycursor.execute("SELECT * FROM ny_faq WHERE bruker_id=%s", (bruker_id))
    ny_q = mycursor.fetchall()

    # mycursor.execute("SELECT * FROM ny_faq")
    # ny_faq = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return render_template("faq_kunde.html", init_q=init_q, ny_q=ny_q)


# !LIBRARIAN!


# LIBRARIAN HOME PAGE
@app.route("/login/homepage_lib")
def homepage_lib():
    if session.get("rolle") == "admin":

        mydb = get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM boker")
        boker = mycursor.fetchall()  # liste??

        mycursor.close()
        mydb.close()

        return render_template("homepage_lib.html", epost=session["epost"], boker=boker)
    return redirect(url_for("login"))


# FULL CUSTOMER OVERVIEW (for librarian)
@app.route("/login/homepage_lib/customers")
def customers():
    if session.get("rolle") == "admin":
        mydb = get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM brukere")
        brukere = mycursor.fetchall()

        mycursor.close()
        mydb.close()

        return render_template("customers.html", brukere=brukere)
    return redirect(url_for("login"))


# siden kræsjet når jeg ville se/sjekke customers,
# så måtte finne ut av hvorfor og en AI sa at det kunne være pga disse
# "if"-setningene om man er admin eller ikke, at man trengte en løsning


# OVERVIEW OF BORROWED BOOKS (for librarian)
@app.route("/login/homepage_lib/overview_lib")
def overview_lib():
    if session.get("rolle") == "admin":
        mydb = get_connection()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM bestilling")
        bestilling = mycursor.fetchall()  # liste??

        mycursor.close()
        mydb.close()

        return render_template("overview_lib.html", bestilling=bestilling)
    return redirect(url_for("login"))


# ADD NEW BOOKS (for librarian)
@app.route("/login/homepage_lib/add_books_lib", methods=["GET", "POST"])
def add_books_lib():

    if session.get("rolle") == "admin":
        if request.method == "POST":

            name = request.form["bok_navn"]
            author = request.form["bok_forfatter"]

            # ![15/3/26]
            copies = request.form["antall_boker"]

            mydb = get_connection()
            mycursor = mydb.cursor()

            mycursor.execute(
                "INSERT INTO boker (bok_navn, bok_forfatter, antall_boker) VALUES (%s, %s, %s)",
                (name, author, copies),
            )
            mydb.commit()
            mycursor.close()
            mydb.close()

            return redirect(url_for("homepage_lib"))
        return render_template(
            "add_books_lib.html",
        )


# ![19/5/26] tirsdag - customer service???
# CUSTOMER SERVICE (for librarian)
@app.route("/login/homepage_lib/faq_lib", methods=["GET", "POST"])
def faq_lib():

    if session.get("rolle") == "admin":
        mydb = get_connection()
        mycursor = mydb.cursor()
        
        # ![19/5/26]
        if request.method == "POST":
            faq_id = request.form["faq_id"]
            svar = request.form["svar"]
            
            mycursor.execute("UPDATE ny_faq SET svar = %s WHERE id=%s", (svar, faq_id))
            
            mydb.commit()
                                                                  # ![20/5/26] for dissapearing stuff
        mycursor.execute("SELECT * FROM ny_faq WHERE bruker_id != 1 AND (svar is NULL)")
        ny_q = mycursor.fetchall()

        mycursor.close()
        mydb.close()

        return render_template("faq_lib.html", ny_q=ny_q)
    return redirect(url_for("login"))


# LIBRARIAN AUTHORITIES

# EDIT CUSTOMER - (for librarian - viser informasjon)


@app.route(
    "/login/homepage_lib/customers/edit_kunde/<int:cid>", methods=["GET", "POST"]
)
def edit_kunde(cid):
    if session.get("rolle") == "admin":

        mydb = get_connection()
        mycursor = mydb.cursor()

        mycursor.execute(
            "SELECT fornavn, etternavn, epost, telefonnummer FROM brukere WHERE id=%s",
            (cid,),
        )

        bruker = mycursor.fetchone()

        mycursor.close()
        mydb.close()

        return render_template("edit_kunde.html", bruker=bruker, cid=cid)
    return redirect(url_for("login"))


@app.route("/customers/update_kunde", methods=["POST"])
def update_kunde():
    cid = request.form["id"]
    fornavn = request.form["fornavn"]
    etternavn = request.form["etternavn"]
    epost = request.form["epost"]
    telefonnummer = request.form["telefonnummer"]

    mydb = get_connection()
    mycursor = mydb.cursor()

    mycursor.execute(
        "UPDATE brukere SET fornavn=%s, etternavn=%s, epost=%s, telefonnummer=%s WHERE id=%s",
        (fornavn, etternavn, epost, telefonnummer, cid),
    )

    mycursor.close()
    mydb.commit()
    mydb.close()

    return redirect(url_for("customers"))


@app.route("/customers/delete_kunde/<int:cid>")
def delete_kunde(cid):
    mydb = get_connection()
    mycursor = mydb.cursor()

    mycursor.execute("DELETE FROM bestilling WHERE bruker_id=%s", (cid,))
    mycursor.execute("DELETE FROM brukere WHERE id=%s", (cid,))

    mydb.commit()
    mydb.close()
    return redirect(url_for("customers"))


if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == '__main__':
#     serve(app, host='0.0.0.0', port=8080)
