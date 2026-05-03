from flask import Flask, request, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "customers.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_customers(keyword=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if keyword:
        cursor.execute(
            "SELECT id, name FROM customers WHERE name LIKE ?",
            ("%" + keyword + "%",)
        )
    else:
        cursor.execute("SELECT id, name FROM customers")

    customers = cursor.fetchall()
    conn.close()

    return customers


def add_customer(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO customers (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()


def update_customer(customer_id, new_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE customers SET name = ? WHERE id = ?",
        (new_name, customer_id)
    )

    conn.commit()
    conn.close()


def delete_customer(customer_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM customers WHERE id = ?", (customer_id,))

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/customers", methods=["GET"])
def customers_api():
    keyword = request.args.get("keyword", "")
    data = get_customers(keyword)

    result = []
    for customer in data:
        result.append({
            "id": customer[0],
            "name": customer[1]
        })

    return jsonify(result)


@app.route("/customers", methods=["POST"])
def add_customer_api():
    data = request.get_json()
    name = data.get("name")

    if name:
        add_customer(name)

    return jsonify({"status": "ok"})


@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer_api(id):
    data = request.get_json()
    new_name = data.get("name")

    if new_name:
        update_customer(id, new_name)

    return jsonify({"status": "ok"})


@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer_api(id):
    delete_customer(id)

    return jsonify({"status": "ok"})


init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)