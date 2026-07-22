"""Q4 (Version 1): search page with input validation per OWASP C5.

- "/"       home page: one search field + submit button
- "/result" shown only when the search term passes validation
"""

import os

from flask import Flask, render_template, request

from validators import validate_search

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        term = request.form.get("search_term", "")
        is_valid, message = validate_search(term)
        if not is_valid:
            # Requirements (c)/(d): clear the input and stay on the home page.
            return render_template("index.html", error=message)
        # Requirements (e)/(f): show the term on a new page.
        return render_template("result.html", term=term)
    return render_template("index.html")


if __name__ == "__main__":
    # Host from env so the bind address is not hard-coded (SonarQube flags a
    # hard-coded 0.0.0.0 bind as a security hotspot). Compose sets FLASK_HOST.
    app.run(host=os.environ.get("FLASK_HOST", "127.0.0.1"), port=5000)
