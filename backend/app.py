from flask import Flask, render_template, request, jsonify, make_response
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

    response, _ = nlp.query_knn('site', 'resource', cohere_util.embed(text))
    message = {"answer": response}
    return jsonify(message)


@app.route("/cookies")
def cookies():
    res = make_response("Cookies", 200)
    res.set_cookie("rss_only", "True")
    res.set_cookie("address", "")

    return res


if __name__ == "__main__":
    app.run(debug=True)
