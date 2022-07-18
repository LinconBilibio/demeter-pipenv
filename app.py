# Python connection for Postgres
# https://devcenter.heroku.com/articles/connecting-heroku-postgres#connecting-in-python
import os
import psycopg2

# Flask
from flask import Flask, render_template, request, redirect, request_tearing_down

# Configures application
app = Flask(__name__)

# Configures database
DATABASE_URL = os.environ["DATABASE_URL"]
conn = None

# Establishes all possible product types for inventory entry
PRODUCT_TYPES = ["Adjuvante", "Fungicida", "Herbicida", "Inseticida", "Óleo"]

# Establishes all possible sellers
SELLERS = ["Coopavel", "DISAM", "I.RIEDI", "Pitangueiras"]


@app.route("/")
def inventory():
    """Shows current inventory"""
    return render_template("inventory.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    """Adds a new entry to inventory"""

    # POST
    if request.method == "POST":
        seller = request.form.get("seller")
        product_name = request.form.get("product_name")
        product_type = request.form.get("product_type")
        product_quantity = int(request.form.get("product_quantity"))
        unit_price = float(request.form.get("unit_price"))
        total_cost = product_quantity * unit_price
        date = request.form.get("date")

        # Adds entry to database
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode="require")
            cur = conn.cursor()

            cur.execute("INSERT INTO purchases (seller, product_name, product_type, product_quantity, unit_price, total_cost, date, user_id) VALUES (%s, %s, %s, %i, %f, %s, %i);", (seller, product_name, product_type, product_quantity, unit_price, total_cost, date, 1))

            cur.close()
        except Exception as error:
            print("Could not connect to the database.")
            print("Cause: {}".format(error))

        # Close communication to database
        if conn is not None:
            conn.close()
            print("Database connection closed.")

        # Redirects user
        return redirect("/")
    
    # GET
    else:
        return render_template("add.html", types=PRODUCT_TYPES, sellers=SELLERS)