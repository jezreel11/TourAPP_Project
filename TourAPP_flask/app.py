from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = "secret-key-here"  # for session management
# URL of your FastAPI backend
API_URL = "http://127.0.0.1:8000/tournaments"
API_USERS = "http://127.0.0.1:8000/users"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        response = requests.post(f"{API_USERS}/login", json={"username": username, "password": password})
        if response.status_code == 200:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        response = requests.post(f"{API_USERS}/register", json={"username": username, "password": password})
        if response.status_code == 200:
            return redirect(url_for("login"))
        else:
            return render_template("register.html", error=response.json().get("detail"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/")
def home():
    try:
        if "user" not in session:
            return redirect(url_for("login"))
        response = requests.get(API_URL)
        tournaments = response.json()
    except Exception as e:
        tournaments = []
        print("Error connecting to API:", e)
    return render_template("index.html", tournaments=tournaments)

@app.route("/add", methods=["POST"])
def add_tournament():
    data = {
        "name": request.form["name"],
        "location": request.form["location"],
        "date": request.form["date"]
    }
    requests.post(API_URL, json=data)
    return redirect(url_for("home"))

@app.route("/delete/<int:id>")
def delete_tournament(id):
    requests.delete(f"{API_URL}/{id}")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
