from flask import Flask
app = Flask(__name__)
@app.route('/')
def back_end():
    return "backend server test"
