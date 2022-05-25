from requests import Response
import re

class PresenceRequest():
    def __init__(self):
        self.azienda = None

    def parseUserInput(self, input_statement: str) -> str:
        # Da vedere se c'è già una richiesta precedente inerente a questo request

        splittedWords = input_statement.split(' ')
        match = splittedWords.index('sede')
        if match + 1 < len(splittedWords):
            self.azienda = splittedWords[match+1]
        # Else manca l'azienda
    
    def isReady(self) -> bool:
        if self.azienda is not None:
            return True
        return False
    
    def parseResult(self, response: Response) -> str:
        if response.status_code == 200:
            str = ""
            for record in response.json():
                str += "\tLocalità: " + record.get('location', "non segnalata") + '\n'
                str += "\tUtente: " + record.get('user', "non registrato") + '\n'
                str += '\n'

            return str
        else: # Da gestire i casi di richiesta non valida
            return "Richiesta non andata a buon fine"