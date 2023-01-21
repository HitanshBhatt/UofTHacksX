from flask import Flask, render_template, request, jsonify
import nlp
import json
import cohere_util


app = Flask(__name__)


@app.get("/")
def index_get():
    return render_template("base.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")

    response, _ = nlp.query_knn('site', cohere_util.embed(text))
    message = {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
