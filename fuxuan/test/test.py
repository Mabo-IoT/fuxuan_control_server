import requests


data = {
    "channel": "TestTemperature",
    "value": 69.5,
    "control": True,
}
r = requests.post('http://127.0.0.1:8000/control', json=data)
print(dir(r))
print(r.content)