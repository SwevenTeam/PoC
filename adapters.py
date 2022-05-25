from operator import truediv
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from request import PresenceRequest
import requests


class PresenceAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.adapter: str = None
        self.request = None
        self.api_key = kwargs.get('secret_key')

    # Serve Levenshtein distance per 'misurare' le parole
    def can_process(self, statement):
        if self.adapter is None:
            words = ['location', 'sede', 'sedi']
            if any(x in statement.text.split() for x in words):
                return True
            else:
                return False
        else:
            return True

    def process(self, input_statement, additional_response_selection_parameters):
        if self.adapter is None:
            self.adapter="PresenceAdapter" # Imposto questo come adapter se posso processare la richiesta
            self.request=PresenceRequest()
        
        response = self.request.parseUserInput(input_statement.text)

        if self.request.isReady():
            url = "https://apibot4me.imolinfo.it/v1/locations/" + self.request.azienda + "/presence"

            responseUrl = requests.get(url, headers={"api_key": self.api_key})
            response_statement = Statement(self.request.parseResult(responseUrl)) # Parse della risposta, da controllare lo status (?)

            #if response.status_code == 200:
            #    confidence = 1
            #else:
            #    confidence = 0

            # Riporto a "zero" i paramentri
            self.adapter = None
            self.request = None

        else:
            response_statement = Statement(response) # Non faccio nulla / passo avanti la response

        return response_statement