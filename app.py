import os

from flask import Flask, url_for, request, render_template, redirect

os.chdir("E:\COURSERA\PythonFlask\week_2\obmnl-flask_assignment")

app = Flask(__name__)

# Sample data
transactions = [
    {"id": 1, "date": "2023-06-01", "amount": 100},
    {"id": 2, "date": "2023-06-02", "amount": -200},
    {"id": 3, "date": "2023-06-03", "amount": 300},
]


@app.route("/", methods=["GET"])
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        transaction = {
            "id": len(transactions) + 1,
            "date": request.form["date"],
            "amount": request.form["amount"],
        }
        transactions.append(transaction)

        return redirect(url_for("get_transactions"))
    return render_template("form.html")


# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id: int):
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)
    if request.method == "POST":
        if not transaction:
            return f"Transaction with id {transaction_id} not found", 404
        else:
            transaction["date"] = request.form["date"]
            transaction["amount"] = float(request.form["amount"])

        return redirect(url_for("get_transactions"))
    return render_template("edit.html", transaction=transaction)


# Delete operation
@app.route("/delete/<int:transaction_id>", methods=["DELETE", "GET"])
def delete_transaction(transaction_id: int):
    transaction = next((t for t in transactions if t["id"] == transaction_id), None)

    if not transaction:
        return f"Transaction with id {transaction_id} not found", 404
    else:
        # del transactions[transaction]
        transactions.remove(transaction)
        return redirect(url_for("get_transactions"))


@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        min_value = float(request.form["min_amount"])
        max_value = float(request.form["max_amount"])

        filtered_transactions = [
            t for t in transactions if min_value <= t["amount"] <= max_value
        ]
        return render_template("transactions.html", transactions=filtered_transactions)
    return render_template("search.html")


@app.route("/balance", methods=["GET"])
def total_balance():
    balance = sum(t["amount"] for t in transactions)
    return f"Total balance: {balance}"


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8080)
