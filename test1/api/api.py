import json
from datetime import datetime

import fastapi
import requests

from db.models import save_data_to_db

URL = 'https://webservicesp.anaf.ro/api/PlatitorTvaRest/v9/tva'
app = fastapi.FastAPI()

def replace_string_to_none(data):
    if isinstance(data, dict):
        return {key: replace_string_to_none(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_string_to_none(item) for item in data]
    elif data == "":
        return None
    else:
        return data

@app.get('/api/{cui}')
def get_data(cui):
    now_date = datetime.now().strftime("%Y-%m-%d")
    response = requests.post(
        URL, 
        json=[{
            "cui":cui,
            "data":now_date
        }], 
        headers={'Content-Type': 'application/json'}
    )
    cleaned_data = replace_string_to_none(response.json())
    db_message = save_data_to_db(cleaned_data)
    message = {"cui":cui, 'db_message':db_message} # cleaned_data['found'][0]['date_generale']:dict.get('cui')
    return message

if __name__ == '__main__':
    # uvicorn.run(app)
    response = get_data(17058074)
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(response, file, ensure_ascii=False, indent=4)