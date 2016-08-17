import redis
import pdb
import requests
from ast import literal_eval
import time
redis_host = "localhost"
redis_port = 6379

class RedisHelper(object):

    def __init__(self):
        redis_client = redis.StrictRedis(host=redis_host,port= redis_port, db=0)
        self.redis_client_object = redis_client

    def re_init_redis(self):
        print 're-init redis'
        time.sleep(30)
        redis_client = redis.StrictRedis(host=redis_host,port= redis_port, db=0)
        self.redis_client_object = redis_client

    def set_redis_hash(self, key, data):
        try:
            self.redis_client_object.hmset(key, data)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            self.redis_client_object.hmset(key, data)

        return

    def get_redis_hash(self, bank_name, city):
        try:
            bank_details = self.redis_client_object.hmget(bank_name, city)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            bank_details = self.redis_client_object.hmget(bank_name, city)
        
        if bank_details[0] is not None:
            return literal_eval(bank_details[0])
        else:
            return []

    def set_redis_list(self, key, list):
        try:
            self.redis_client_object.rpush(key, list)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            self.redis_client_object.rpush(key, list)
        return

    def get_redis_list(self, bank_name, start_index = 0, end_index = -1):
        try:
            bank_cities = self.redis_client_object.lrange(bank_name, start_index, end_index)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            bank_cities = self.redis_client_object.lrange(bank_name, start_index, end_index)

        if bank_cities:
            bank_cities = literal_eval(bank_cities[0])
            return bank_cities
        else:
            return []

    #Assign Equal weightage to all keywords(0), dict_seq {value:score}
    def set_sorted_list(self, key, dict_seq):
        try:
            self.redis_client_object.zadd(key, **dict_seq)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            self.redis_client_object.zadd(key, **dict_seq)


    def get_sorted_list(self, key, start_index = 0, end_index = -1):
        try:
            return self.redis_client_object.zrange(key, start_index, end_index)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            return self.redis_client_object.zrange(key, start_index, end_index)

    def get_sorted_lex_string(self, key, min_str, max_str):
        try:
            return self.redis_client_object.zrevrangebylex(key, min_str, max_str)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            return self.redis_client_object.zrevrangebylex(key, min_str, max_str)
        


    def clean_redis_data(self):
        clean = self.redis_client_object.flushall()
        print "junk- cleaned {clean}".format(clean = clean)