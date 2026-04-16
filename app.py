from flask import Flask, request

app = Flask(__name__)

def load_customers():
    customers = []
    try:
        with open("customers.txt", "r", encoding="utf-8") as file:
            for line in file:
                name = line.strip()
                if name != "":
                    customers.append(name)
    except FileNotFoundError:
        pass
    return customers

def save_customer(name):
    with open("customers.txt", "a", encoding="utf-8") as file:
        file.write(name + "\n")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        if name != "":
            save_customer(name)

    customers = load_customers()

    customer_list = ""
    for customer in customers:
        customer_list += f"<li>{customer}</li>"

    return f"""
    <h1>LiGA大会管理ツール</h1>
    <form method="POST">
        名前: <input type="text" name="name">
        <input type="submit" value="登録">
    </form>

    <h2>顧客リスト</h2>
    <ul>
        {customer_list}
    </ul>
    """

if __name__ == "__main__":
    app.run(debug=True)