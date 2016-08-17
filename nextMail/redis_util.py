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

    def get_redis_hash(self, key, key_2 = -1):
        try:
            if key_2 not in [-1]:
                return_hash = self.redis_client_object.hmget(key, key_2)
            else:
                return_hash = self.redis_client_object.hgetall(key)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            if key_2 not in [-1]:
                return_hash = self.redis_client_object.hmget(key, key_2)
            else:
                return_hash = self.redis_client_object.hgetall(key)
        
        return return_hash

    def set_redis_list(self, key, list):
        try:
            self.redis_client_object.rpush(key, list)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            self.redis_client_object.rpush(key, list)
        return

    def get_redis_list(self, key, start_index = 0, end_index = -1):
        try:
            return_list = self.redis_client_object.lrange(key, start_index, end_index)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            return_list = self.redis_client_object.lrange(key, start_index, end_index)

        return return_list

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
            return self.redis_client_object.zrangebylex(key, min_str, max_str)
        except redis.exceptions.ConnectionError:
            self.re_init_redis()
            return self.redis_client_object.zrangebylex(key, min_str, max_str)
        


    def clean_redis_data(self):
        clean = self.redis_client_object.flushall()
        print "junk- cleaned {clean}".format(clean = clean)