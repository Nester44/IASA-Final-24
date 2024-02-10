from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)


@app.route("/", methods=["GET"])
@cross_origin()
def hello_world():
    return jsonify({"message": "Hello, World!"})


if __name__ == "__main__":
    app.run(debug=True)
