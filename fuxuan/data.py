import logging
import json
import falcon


from lib.redis_wrapper import RedisWrapper

log = logging.getLogger('control_server')

class Control:
    def __init__(self, conf):
        self.redis = RedisWrapper(conf)

    def on_post(self, req, resp):
        # get request json data

        data = json.loads(req.stream.read())
        # data = req.stream.read()

        log.info("set data is {}".format(data))
        # check remote lock is on or off
        contorl_lock = self.get_lock_status()
        
        log.info("remote lock status is {}".format(contorl_lock))
        # remote lock is on can't remote control
        if contorl_lock == 1:
            resp.body = "Remote lock is on!"
            resp.status = falcon.HTTP_403

        # remote lock is off 
        else:
            # parse request json to order json
            
            valid = self.__check(data)
            
            # set value is valid
            if valid:
                # set order json in redis
                order_json = self.__parse_data_to_order(data)
                self.__set_order_json(order_json)

                resp.body = "Order send in redis queue, wait for process"
                resp.status = falcon.HTTP_200
            
            # set value is not valid
            else:
                resp.body = "please check your set channel name or value if valid"
                resp.status = falcon.HTTP_403

    def __check(self, order_json):
        """
        check order if valid
        """
        channels = ["TestTemperature", "MaintainTemperature", "AgeingTemperature",
        "ExhaustTime", "AgeingTime", "CoolingTime", "TestTime",]

        ranges = {
            "TestTemperature": [0, 70.0],
            "MaintainTemperature": [0, 70.0], 
            "AgeingTemperature": [10.0, 70.0],
            "ExhaustTime": [1, 9999], 
            "AgeingTime": [1, 9999], 
            "CoolingTime": [1, 9999], 
            "TestTime": [1, 9999],
        }
        log.debug(order_json)
        if order_json['channel'] not in channels:
            return False
        else:
            value = order_json['value']
            channel = order_json['channel']
            range = ranges[channel]
            return self.__if_in_list(value, range)

    @staticmethod
    def __if_in_list(value, range_list):
        """
        check value if in rane_list
        """       
        if value >= range_list[0] and value <= range_list[1]:
            return True
        else:
            return False
    
    def get_lock_status(self):
        """
        get control lock status 
        1: remote control is prohibited
        0: remote control is allowed
        """
        lock_status = self.redis.get("remote_lock")
        return lock_status
    
    
    def __set_order_json(self, order_json):
        """
        set control data in redis
        """
        order_json  = json.dumps(order_json)
        return self.redis.lpush("order_queue", order_json)
    
    def __parse_data_to_order(self, data): 
        """
        parse request json data to redis order
        """
        redis_json = {
            "type": self.__get_type(data['channel']),
            "address": self.__get_address(data['channel']),
            "value": self.__set_value(data)
        }
        return redis_json

    @staticmethod
    def __set_value(data):
        """
        value must be a int
        """
        float_list = ["TestTemperature", "MaintainTemperature", "AgeingTemperature",]
        
        if data['channel'] in float_list:
            value = int(data['value']*10)
        else:
            value = int(data['value'])
        
        return value

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
        

    

        