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
@app.route("/edit/<int:transaction_id>", methods=["PUT", "POST"])
def edit_transaction():
    if request.method == "POST":
        transaction_id = request.args.get("transaction_id")
        
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["date"] = request.form["date"]
                transaction["amount"] = float(request.form["amount"])
                break
        
        return redirect(url_for("get_transactions"))
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction=transaction)


# Delete operation
@app.route("/delete/<int:transaction_id>", methods=["DELETE", "GET"])
def delete_transaction():
    pass


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=8080)
