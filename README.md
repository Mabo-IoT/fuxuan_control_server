## A control server
A falcon server to control modbus device.

## Usage:
- 1. change ```conf/conf.toml``` to suit your case
- 2. ```cd fuxuan``` 
- 3.```python app.py``` to open your server
- 4. then Post json data to "http://yourip:yourport/control"
- 5. json example ```{'channel': 'TestTemperature', 'value': 69.0, 'control': True}```
