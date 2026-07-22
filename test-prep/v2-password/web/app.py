"""Q4 (Version 2): password login page validated against OWASP C6 Level 1.

- GET  "/"        home page: one password field + login button
- POST "/login"   validates the password (safe GET / unsafe POST kept separate)
- "/welcome"      shown only when the password meets the requirements
- "/logout"       returns to the home page
"""

import os

from flask import Flask, redirect, render_template, request, session, url_for

from validators import validate_password

app = Flask(__name__)
# Secret comes from the environment; the default is for local dev only.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password", "")
    is_valid, message = validate_password(password)
    if not is_valid:
        # Requirement (e): stay on the home page.
        return render_template("index.html", error=message)
    # Requirement (f): go to the Welcome page.
    session["password"] = password
    return redirect(url_for("welcome"))


@app.route("/welcome")
def welcome():
    password = session.get("password")
    if not password:
        return redirect(url_for("home"))
    return render_template("welcome.html", password=password)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    # Host from env so the bind address is not hard-coded (SonarQube flags a
    # hard-coded 0.0.0.0 bind as a security hotspot). Compose sets FLASK_HOST.
    app.run(host=os.environ.get("FLASK_HOST", "127.0.0.1"), port=5000)
