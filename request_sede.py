from requests import Response
import json
from flask import session


class request_sede():
    def __init__(self):
        self.azienda = None

    def parseUserInput(self, input_statement: str) -> str:
        # Tolgo lo spit perché la mia stringa non è univoca
        if session['status'] == "location":
            # Questo controllo per ora non serve, visto che inserisce in 2
            # "andate/messaggi" diverse/i
            self.azienda = input_statement
        else:
            # Il codice di Mattia controlla che dopo la parola sede venga
            # inserito il luogo
            if session['status'] == "sede_location":
                splittedWords = input_statement.split(' ')
                match = splittedWords.index('sede')
                if match + 1 < len(splittedWords):
                    # Prende solo la parola dopo
                    # Se si scrive "dammi sede bologna" funziona
                    # Se si scrive "dammi la sede di bologna" non funziona
                    self.azienda = splittedWords[match + 1]

    def isReady(self) -> bool:
        if self.azienda is not None:
            return True
        return False

    def parseResult(self, response: Response) -> str:
        if response.status_code == 200:
            out_str = ""
            for record in response.json():
                out_str += "\tLocalità: " + \
                    str(record.get('location', "non segnalata")) + '\n'
                out_str += "\tUtente: " + \
                    str(record.get('user', "non trovato")) + '\n'
                out_str += '\n'

            # Se la richiesta funziona, setto status a ""
            session['status'] = ""
            if out_str == "":
                out_str ="Richiesta andata a buon fine, ma nessun dato da visualizzare"
            return out_str
        else:  # Da gestire i casi di richiesta non valida
            return "Richiesta non andata a buon fine"
