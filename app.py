from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# 顧客読み込み
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

# 顧客保存
def save_customer(name):
    with open("customers.txt", "a", encoding="utf-8") as file:
        file.write(name + "\n")

# メイン画面
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            save_customer(name)
        return redirect("/")

    customers = load_customers()
    return render_template("index.html", customers=customers)


if __name__ == "__main__":
    app.run(debug=True)