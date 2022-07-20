import json

from fastapi import FastAPI
import logging
import urllib
import google.auth.transport.requests
import google.oauth2.id_token
import os
from google.cloud import storage

app = FastAPI()


@app.get("/")
async def root():
    service_url = 'https://grad-forecast-api-ist6wm4moa-nw.a.run.app/api/v1/projects'
    req = urllib.request.Request(service_url)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)
    req.add_header("Authorization", f"Bearer {id_token}")
    try:
        response = urllib.request.urlopen(req)
        resp_content = response.read()
        pretty_resp = json.dumps(resp_content, indent=2)
        staging_bucket_name = os.environ.get('STAGING_BUCKET')
        client = storage.Client()
        bucket = client.bucket(staging_bucket_name)
        blob = bucket.blob('projects.json')
        blob.upload_from_string(data=pretty_resp, content_type='application/json')
        return {
            "message": "Forecast API call happy"
        }
    except BaseException as e:
        print(f"Problem with the URL. Response: {e}")
        return {
            "message": f"Forecast API call sad: {e}"
        }


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
