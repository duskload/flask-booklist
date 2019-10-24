import os

from flask import Flask, session, render_template, request, redirect
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Get goodreads api key
if not os.getenv("GOODREADS_API_KEY"):
    raise RuntimeError("GOODREADS_API_KEY is not set")

@app.route("/", methods=['POST', 'GET'])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')

    if session.get("user") is None:
        session["user"] = {}

    user = db.execute("SELECT * FROM users WHERE password = :password AND username = :username", { "username": username, "password": password }).fetchone()

    if user:
        session["user"] = { "id": user[0], "username": user[1] }
        return redirect('/dashboard')

    return render_template("signin.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')


    # do registration
    if username and password:
        if db.execute("SELECT * FROM users WHERE password = :password AND username = :username", { "username": username, "password": password }).fetchone() is None:
            db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", { "username": username, "password": password })

            db.commit()
    
    return render_template("signup.html")

@app.route('/logout')
def logout():
    session['user'] = {}
    return redirect('/')


@app.route("/dashboard")
def dashboard():
    user = session.get("user")

    if user is not None:
        return render_template('dashboard.html')
    
    return redirect('/')

@app.route("/search", methods=["POST"])
def search():
    if request.method == "POST":
        query = request.form.get('search')

        if query is not None:
            values = db.execute("SELECT * FROM books WHERE year LIKE :query OR title LIKE :query OR isbn LIKE :query", {
                "query": f"%{query}%"
            }).fetchall()

            if len(values) == 0:
                values = [{ "title": "No matches found" }]

            return render_template('dashboard.html', values=values)

    # return a message that search gives null results
    return render_template('dashboard.html')

    