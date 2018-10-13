from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("skor")
db = SQLAlchemy(app)

user = {
	"id": 1,
	"skor": 0
}

@app.route("/")
def index_page():
	if request.method == "POST":
		
	return render_template("skor.html")


