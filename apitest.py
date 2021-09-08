import requests
import json
import io


api_url = "http://sea-shanty-api.herokuapp.com"
api_url_local = "http://localhost:3000"
api_url_all = api_url + "/shanties/all"
api_url_local_all = api_url_local + "/shanties/all"

resp = requests.get(url=api_url_local_all)
my_json = json.load(io.BytesIO(resp.content))

for title in my_json['shanties']:
    url = api_url_local + "/shanties?title=" + title
    resp = requests.get(url=url)
    my_json = json.load(io.BytesIO(resp.content))
    try:
        my_json['shanty']
    except KeyError:
        print(my_json['error'], my_json['title'])
