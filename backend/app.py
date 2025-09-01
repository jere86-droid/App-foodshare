from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for sessions

users = {}  # fake "database" (in-memory)

@app.route("/")
def home():
    if "user" in session:
        return f"Welcome back, {session['user']}! <a href='/logout'>Logout</a>"
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        users[email] = password
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if email in users and users[email] == password:
            session["user"] = email  # ✅ store login in session
            return redirect(url_for("home"))
        else:
            return "Invalid credentials, try again."
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)  # ✅ remove user from session
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)

