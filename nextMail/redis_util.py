import redis
import pdb
import requests
from ast import literal_eval

redis_host = "localhost"
redis_port = 6379

class RedisHelper(object):

    def __init__(self):
        redis_client = redis.StrictRedis(host=redis_host,port= redis_port, db=0)
        self.redis_client_object = redis_client

    def set_redis_hash(self, key, data):
        self.redis_client_object.hmset(key, data)
        return

    def get_redis_hash(self, bank_name, city):
        bank_details = self.redis_client_object.hmget(bank_name, city)
        if bank_details[0] is not None:
            return literal_eval(bank_details[0])
        else:
            return []

    def set_redis_list(self, key, list):
        self.redis_client_object.rpush(key, list)
        return

    def get_redis_list(self, bank_name, start_index = 0, end_index = -1):
        bank_cities = self.redis_client_object.lrange(bank_name, start_index, end_index)
        if bank_cities:
            bank_cities = literal_eval(bank_cities[0])
            return bank_cities
        else:
            return []
