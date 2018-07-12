import requests


data = {
    "channel": "TestTemperature",
    "value": 79.0,
    "control": True,
}
r = requests.post('http://127.0.0.1:8000/control', json={"channel": "test", "value":79.0, "control":True})
print(dir(r))
print(r.content)