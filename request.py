from requests import Response
import json

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
            out_str = ""
            for record in response.json():
                out_str += "\tLocalità: " + str(record.get('location', "non segnalata")) + '\n'
                out_str += "\tUtente: " + str(record.get('user', "non trovato")) + '\n'
                out_str += '\n'

            return out_str
        else: # Da gestire i casi di richiesta non valida
            return "Richiesta non andata a buon fine"