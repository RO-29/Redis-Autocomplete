import redis
import pdb
import requests

redis_host = "localhost"
redis_port = 6379

class RedisHelper(object):

    def __init__(self, app):
        app.redis = redis.StrictRedis(host=redis_host,port= redis_port, db=0)
        self.redis_client_object = app.redis

    