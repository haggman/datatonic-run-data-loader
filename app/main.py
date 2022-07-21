import json

from fastapi import FastAPI
import logging
import urllib.request
import google.auth.transport.requests
import google.oauth2.id_token
import os
from google.cloud import storage

app = FastAPI()


@app.get("/")
async def root():
    def api_call_helper(api_path, file_name):
        service_url = f'https://grad-forecast-api-ist6wm4moa-nw.a.run.app/api{api_path}'
        req = urllib.request.Request(service_url)
        auth_req = google.auth.transport.requests.Request()
        id_token = google.oauth2.id_token.fetch_id_token(auth_req, service_url)
        req.add_header("Authorization", f"Bearer {id_token}")
        # Get the Projects JSON from the Forecast API
        response = urllib.request.urlopen(req)
        resp_content = response.read().decode()
        # Convert from array of objects to JSONL format
        file_json = json.loads(resp_content)
        json_list = [json.dumps(record) for record in file_json]
        text_jsonl_str = '\n'.join(json_list)
        # Upload to GCS
        staging_bucket_name = os.environ.get('STAGING_BUCKET')
        client = storage.Client()
        bucket = client.bucket(staging_bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(data=file_json, content_type='application/json')

    try:
        # api_call_helper('/v1/projects', 'projects.json')
        api_call_helper('/v4/tasks', 'tasks.json')
        return {
            "message": "Forecast API call happy"
        }
    except BaseException as e:
        print(f"Problem with the URL. Response: {e}")
        return {
            "message": f"Forecast API call sad: {e}"
        }
