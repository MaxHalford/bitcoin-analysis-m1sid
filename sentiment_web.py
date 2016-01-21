import requests

headers = {'content-type': 'application/json'}

data = {
    'text': ':('
}

url = 'http://text-processing.com/api/sentiment/'

r = requests.post(url, data=data, headers=headers)

print(r.json())
