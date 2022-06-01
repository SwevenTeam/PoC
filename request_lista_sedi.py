from requests import Response
import json
from flask import session


class request_lista_sedi():

    def parseUserInput(self, input_statement: str) -> str:
        if session['status'] == "lista_sedi":
            splittedWords = input_statement.split(' ')
            match = splittedWords.index('lista')
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
                    str(record.get('name', "non segnalata")) + '\n'
                out_str += "\tUtente: " + \
                    str(record.get('address', "non trovato")) + '\n'
                out_str += '\n'

            # Se la richiesta funziona, setto status a ""
            session['status'] = ""
            return out_str
        else:  # Da gestire i casi di richiesta non valida
            return "Richiesta non andata a buon fine"
