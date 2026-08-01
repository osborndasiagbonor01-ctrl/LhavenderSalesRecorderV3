from flask import Flask, render_template, request, redirect
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = "sales.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as file:
        sales = json.load(file)
else:
    sales = []

def save_sales():
    with open(DATA_FILE, "w") as file:
        json.dump(sales, file, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        product = request.form["product"]
        quantity = int(request.form["quantity"])
        price = float(request.form["price"])
        total = quantity * price

        sales.append({
            "product": product,
            "quantity": quantity,
            "price": price,
            "total": total,
            "date": datetime.now().strftime("%d-%m-%Y %H:%M")
        })

        save_sales()
        return redirect("/")

    grand_total = sum(item["total"] for item in sales)

    return render_template("index.html", sales=sales, grand_total=grand_total)

@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(sales):
        sales.pop(index)
        save_sales()
    return redirect("/")

@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    if index < 0 or index >= len(sales):
        return redirect("/")

    sale = sales[index]

    if request.method == "POST":
        sale["product"] = request.form["product"]
        sale["quantity"] = int(request.form["quantity"])
        sale["price"] = float(request.form["price"])
        sale["total"] = sale["quantity"] * sale["price"]

        save_sales()
        return redirect("/")

    return render_template("edit.html", sale=sale, index=index)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
