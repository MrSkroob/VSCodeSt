from flask import Flask, request, abort, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello")
def hello():
    return "Hello!"


@app.route("/add")
def add():
    a = request.args.get("first", "")
    b = request.args.get("second", "")
    if a and b:
        try: 
            result = int(a) + int(b)
        except ValueError:
            return abort(400, description="Invalid arguments")
        return f"{a} + {b} = {result}"
    else:
        return abort(400, description="Missing arguments")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)