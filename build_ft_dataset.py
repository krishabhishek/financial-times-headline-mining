import requests
import json
import math
import time
import logging

logging.basicConfig(level=logging.INFO)

url = "http://api.ft.com/content/search/v1"
result_count = 100
with open("credentials/api_key.json") as key_file:
    querystring = json.load(key_file)
offset = 0
payload = \
    {
        "queryString": "lastPublishDateTime:>2012-01-01T00:00:00Z + \
            lastPublishDateTime:<2017-01-01T00:00:00Z",
        "queryContext": {"curations": ["ARTICLES"]},
        "resultContext": {"offset": offset, "aspects": ["title", "lifecycle"]}
    }

headers = {"content-type": "application/json"}

response = \
    requests.request(
        "POST", url, data=json.dumps(payload),
        headers=headers, params=querystring
    )

output_file_path = "/home/v2john/news.txt"

results_dict = json.loads(response.text)['results'][0]
totalResults = results_dict['indexCount']
callsToMake = math.ceil(totalResults / result_count)

for offset in range(callsToMake):
    logging.info("Offset: " + str(offset))

    payload = \
        {
            "queryString": "lastPublishDateTime:>2012-01-01T00:00:00Z \
                lastPublishDateTime:<2017-01-01T00:00:00Z",
            "queryContext": {"curations": ["ARTICLES"]},
            "resultContext": {
                "offset": offset,
                "aspects": ["title", "lifecycle"]
            }
        }
    response = \
        requests.request(
            "POST", url, data=json.dumps(payload),
            headers=headers, params=querystring
        )
    results_list = json.loads(response.text)['results'][0]['results']

    with open(output_file_path, "a+") as output_file:
        for result in results_list:
            headline = dict()
            headline['title'] = result['title']['title']
            headline['publishTime'] = \
                result['lifecycle']['lastPublishDateTime']
            output_file.write(json.dumps(headline) + "\n")

    time.sleep(5)
