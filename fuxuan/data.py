import json
import falcon

from Doctopus.lib.database_wrapper import RedisWrapper


class Resource:
    def on_get(self, req, resp):
        doc = {
            'images':[
                {
                    'href': '/images/123.png'
                }
            ]
        }
    
        resp.body = json.dumps(doc, ensure_ascii=False)

        resp.status = falcon.HTTP_200


class Control:
    def __init__(self, conf):
        self.redis = RedisWrapper(conf['redis'])

    def on_post(self, req, resp):
        # get request json data
        data = json.loads(req.context)
    
    def set_order_json(self, order_json):
        """
        set control data in redis
        """




    @staticmethod
    def __get_type(channel_name):
        """
        get redis json type name
        """

        holding_registers_names = ["TestTemperature", "MaintainTemperature", "AgeingTemperature",
        "ExhaustTime", "AgeingTime", "CoolingTime", "TestTime",]

        if channel_name in holding_registers_names:
            return "holding_registers"
        else:
            return None
    
    @staticmethod
    def __get_address(channel_name):
        """
        get redis json address
        """
        address_dicts = {
            "TestTemperature": 0x11a4,
            "MaintainTemperature": 0x11a5,
            "AgeingTemperature": 0x11a6,
            "ExhaustTime": 0x119a,
            "AgeingTime": 0x119c,
            "CoolingTime": 0x119e,
            "TestTime": 0x11a0,
        } 

        return address_dicts.get(channel_name, None)
        
    def parse_data_to_order(self, data): 
        """
        parse request json data to redis order
        """
        redis_json = {
            "type": self.__get_type(data['channel_name']),
            "address": self.__get_address(data['channel_name']),
            "value": data['value']
        }
        return redis_json

    

        