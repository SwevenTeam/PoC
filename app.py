import json
import string
from urllib.request import HTTPBasicAuthHandler
from numpy import rec
from requests.auth import HTTPBasicAuth
from chatterbot import ChatBot
import requests
from requests.structures import CaseInsensitiveDict
from chatbot import chatbot
from flask import Flask, render_template, request

app = Flask(__name__)
app.static_folder = 'static'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    if(userText == 'Sedi'):
        location_info = get_location_info();
        if(location_info) is not None:
            return str(location_info)
        else:
            print('[!] Richiesta fallita')
    return str(chatbot.get_response(userText))

def get_location_info():
    api_token = '12345678-1234-1234-1234-123456789012'
    api_url_base = 'https://apibot4me.imolinfo.it/v1/locations'
    headers=CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["api_key"] = api_token;
    response = requests.get(api_url_base,headers=headers)
    
    str_to_return=""
    if response.status_code == 200:
        data = response.json()
        for items in data:
            str_to_return+="<strong>Nome azienda: </strong>"+items['name']
            str_to_return+="<br/>"
            str_to_return+="<strong>Indirizzo: </strong>"+items['address']
            str_to_return+="<br/>"
        
        return str_to_return;
        # return response.content.decode('utf-8')
    else:
        return None

if __name__ == "__main__":
    app.run()