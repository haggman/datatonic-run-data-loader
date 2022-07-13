from fastapi import FastAPI
import logging
import urllib
import google.auth.transport.requests
import google.oauth2.id_token

app = FastAPI()


@app.get("/")
async def root():
    service_url = 'https://grad-forecast-api-ist6wm4moa-nw.a.run.app/'
    req = urllib.request.Request(service_url)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)
    req.add_header("Authorization", f"Bearer {id_token}")
    try:
        response = urllib.request.urlopen(req)
        logging.info('Response: ', response.read())
        return {"message": "Forecast API call success"}
    except:
        return {
            "message": "Error calling Forecast API"
        }


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
