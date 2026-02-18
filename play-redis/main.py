import redis

r = redis.Redis(host="localhost", port=6379, db=0)


def init():
    result = r.mget("user:3", "user:4")
    print(f"redis result : {result}")


init()
