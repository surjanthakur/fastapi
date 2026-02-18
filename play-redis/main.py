import redis

r = redis.Redis(host="localhost", port=6379, db=0)


def init():
    result = r.set("msg:1", "hy from python")
    print(f"redis result : {result}")


init()
