from operator import truediv
import chatterbot
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from request_sede import request_sede
import requests
from flask import session


class adapter_sede(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.api_key = kwargs.get('secret_key')
        self.adapter: str = None

    def can_process(self, statement):
        # Se il valore di global è già sede, vuol dire che è stato inserito
        # sede e cerca la posizione

        # Setto i parametri con cui cercare
        locations = ['bologna', 'imola']
        words = ['sede', 'sedi']
        not_words = ['lista','elenco','liste']

        if session['status'] == "sede":
            if any(x in statement.text.split() for x in locations):
                # Aggiorno lo status di conseguenza
                session['status'] = "location"
                return True
            else:
                return False
        # Se il valore di global non è sede, allora controlla se è stato
        # scritto sede
        else:
            if any(x in statement.text.split() for x in words) and not any(x in statement.text.split() for x in not_words):
                # Aggiorno lo status di conseguenza
                session['status'] = "sede"
                if any(x in statement.text.split() for x in locations):
                    # Aggiorno lo status di conseguenza
                    session['status'] = "sede_location"
                    return True
                return True
            else:
                return False

    def process(
            self,
            input_statement,
            additional_response_selection_parameters):
        if self.adapter is None:
            # Imposto questo come adapter se posso processare la richiesta
            self.adapter = "adapter_sede"
            self.request = request_sede()

        # Se entra in questa funzione e lo status è sede, vuol dire che è appensa stata insirita una sede
        # In questo caso, il bot dovrà rispondere di inserire una sede
        # In una versione più avanzata, si dovrà controllare che non ci sia già
        # scritto "Sede Imola"
        if session['status'] == "sede":
            response = "Inserisci la sede di cui vuoi conoscere le informazioni"
        else:
            response = self.request.parseUserInput(input_statement.text)

        if self.request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/locations/" + \
                self.request.azienda + "/presence"

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

        else:
            # Non faccio nulla / passo avanti la response
            response_statement = Statement(response)

        return response_statement
