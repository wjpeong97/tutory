from app import app
from flask import render_template

@app.route("/classroom")
def classroom():
    return render_template('videoroomtest.html')
