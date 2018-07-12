import logging
import time

import redis
import requests

log = logging.getLogger(__name__)


class RedisWrapper:
    """
    包装 redis 库, 用 lua 脚本作为入队筛选机制

    用法：
    db = database_wrapper.RedisWrapper(conf)
    db.script_load(lua_file)
    db.enqueue(**kwargs)  #入队
    """

    def __init__(self, conf):
        """
        :param conf: dict, 包含 Redis 的 host, port, db
        """
        pool = redis.ConnectionPool(
            host=conf.get('host', 'localhost'),
            port=conf.get('port', 6379),
            db=conf.get('db', 0))
        self.__db = redis.StrictRedis(connection_pool=pool, socket_timeout=1)

        # 测试redis连通性
        self.test_connect()

    def test_connect(self):
        """
        初始化连接 Redis 数据库, 确保 redis 连接成功 
        :return: None
        """
        while True:
            try:
                self.__db.ping()
                return True
            except Exception as e:
                log.error('\n%s', e)
                time.sleep(2)
                continue
    
    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        set data to redis
        """
        return self.__db.set(name, value, ex=None, px=None, nx=False, xx=False)
    
    def get(self, key):
        """
        get data from redis
        """
        return self.__db.get(key)

    def lpush(self, key, value):
        return self.__db.lpush(key,value)
