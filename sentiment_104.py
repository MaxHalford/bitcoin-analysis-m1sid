import requests

headers = {'content-type': 'application/json'}

data = {
    'appid': 'maxhalford25@gmail.com',
    'data': [
        {'text': 'I love Titanic.'}
    ]
}

url = 'http://www.sentiment140.com/api/bulkClassifyJson'

r = requests.post(url, data={'data': [{'text': 'I love Titanic.'}]}, headers=headers)

print(r.status_code)
print(r.text)
