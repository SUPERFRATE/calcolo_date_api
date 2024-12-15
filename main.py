from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI()

class DateRequest(BaseModel):
    text: str

def prossima_settimana(giorno_settimana, riferimento=None):
    if riferimento is None:
        riferimento = datetime.now()
    giorno_attuale = riferimento.weekday()
    giorni_da_aggiungere = (giorno_settimana - giorno_attuale) % 7
    if giorni_da_aggiungere == 0:
        giorni_da_aggiungere = 7
    return riferimento + timedelta(days=giorni_da_aggiungere)

def interpreta_data(richiesta):
    richiesta = richiesta.lower().strip()
    oggi = datetime.now()

    giorni_settimana = {
        'lunedì': 0,
        'lunedi': 0,
        'martedì': 1,
        'martedi': 1,
        'mercoledì': 2,
        'mercoledi': 2,
        'giovedì': 3,
        'giovedi': 3,
        'venerdì': 4,
        'venerdi': 4,
        'sabato': 5,
        'domenica': 6
    }

    if richiesta == 'oggi':
        return oggi
    elif richiesta == 'domani':
        return oggi + timedelta(days=1)
    elif richiesta == 'ieri':
        return oggi - timedelta(days=1)
    else:
        if 'prossimo' in richiesta or 'prossima' in richiesta:
            parole = richiesta.split()
            for parola in parole:
                if parola in giorni_settimana:
                    return prossima_settimana(giorni_settimana[parola], oggi)
        return None

@app.post("/interpreta-data")
def interpreta_data_endpoint(req: DateRequest):
    data = interpreta_data(req.text)
    if data is None:
        return {"error": "Data non riconosciuta"}
    else:
        # Restituiamo la data in un formato YYYY-MM-DD
        return {"date": data.strftime("%Y-%m-%d")}
