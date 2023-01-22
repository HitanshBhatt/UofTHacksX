from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def back_end():
    return "backend server test"


@app.route("/cookies")
def cookies():
    res = make_response("Cookies", 200)
    res.set_cookie("rss_only", "True")
    res.set_cookie("address", "")

    return res
