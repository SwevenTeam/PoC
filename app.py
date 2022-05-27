
from flask import Flask, render_template, request
from chatbot import chatbot
import globals

app = Flask(__name__)


@app.route("/")
def home():
  # Inizzializzo lo status che terrà conto dello stato di operazioni che richiedono input multipli
  globals.initialize()
  return render_template("index.html")


@app.route("/get")
def get_bot_response():
  userText = request.args.get('msg')
  return str(chatbot.get_response(userText))


if __name__ == "__main__":
  app.run()
