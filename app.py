from flask import Flask, render_template

# Configure application
app = Flask(__name__)

@app.route("/")
def layout():
    return render_template("inventory.html")