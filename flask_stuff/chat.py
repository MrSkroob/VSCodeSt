import datetime
from flask import Flask, request, render_template, redirect


app = Flask(__name__)


def get_chat_data():
    with open("messages.txt", "r") as f:
        return f.readlines()


def update_chat_data(message: str):
    with open("messages.txt", "a") as f:
        f.write(message + "\n")


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        name = request.form["Alias"]
        if name == "":
            name = "Anonymous"
        message = request.form["Message"]
        text = f"From {name} at {datetime.datetime.today().strftime('%d/%m/%Y')} {message}"
        update_chat_data(text)
        return redirect("/")
    else:
        chat_data = get_chat_data()
        return render_template("chat.html", messages=chat_data)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)