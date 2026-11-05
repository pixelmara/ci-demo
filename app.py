from flask import Flask, jsonify

app = Flask(__name__)


def add(a, b):
    return a + b


@app.route("/")
def index():
    return jsonify(status="ok", message="Hello from CI/CD!")


@app.route("/add/<int:a>/<int:b>")
def add_route(a, b):
    return jsonify(result=add(a, b))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
