from operator import truediv
import chatterbot
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from request_lista_sedi import request_lista_sedi
import requests
from flask import session


class adapter_lista_sedi(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.api_key = kwargs.get('secret_key')
        self.adapter: str = None

    def can_process(self, statement):
        # Se il valore di global è già sede, vuol dire che è stato inserito
        # sede e cerca la posizione

        # Setto i parametri con cui cercare
        words = ['lista', 'elenco']

        if session['status'] != "lista_sedi":
            if any(x in statement.text.split() for x in words):
                # Aggiorno lo status di conseguenza
                session['status'] = "lista_sedi"
                return True
            else:
                return False

    def process(
            self,
            input_statement,
            additional_response_selection_parameters):
        if self.adapter is None:
            # Imposto questo come adapter se posso processare la richiesta
            self.adapter = "adapter_lista_sedi"
            self.request = request_lista_sedi()

        # Se entra in questa funzione e lo status è sede, vuol dire che è appensa stata insirita una sede
        # In questo caso, il bot dovrà rispondere di inserire una sede
        # In una versione più avanzata, si dovrà controllare che non ci sia già
        # scritto "Sede Imola"
        if session['status'] != "lista_sedi":
            response = self.request.parseUserInput(input_statement.text)

        url = "https://apibot4me.imolinfo.it/v1/locations/"

        responseUrl = requests.get(url, headers={"api_key": self.api_key})
        # Parse della risposta, da controllare lo status (?)
        response_statement = Statement(
            self.request.parseResult(responseUrl))

        # if response.status_code == 200:
        #  confidence = 1
        # else:
        #  confidence = 0

        # Riporto a "zero" i paramentri
        self.adapter = None
        self.request = None

        return response_statement
