
from webbrowser import get
from flask import Flask, render_template, request, session
from chatbot import chatbot

app = Flask(__name__)
app.secret_key = 'secret'


@app.route("/")
def home():
    # Inizzializzo lo status che terrà conto dello stato di operazioni che
    # richiedono input multipli
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    if not session['status']:
        session['status'] = ""
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText))


if __name__ == "__main__":
    app.run()
