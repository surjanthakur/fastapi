import redis

r = redis.Redis(host="localhost", port=6379, db=0)


def init():
    result = r.set("user:12", "ram")  # set the single value string

    r.get("user:12")  # get the single value

    r.mset(
        {"user:1": "mike", "user:2": "roy", "user:3": "james"}
    )  # set multiple values at one time
    r.mget({"user:1", "user:2", "user:12"})  # get multiple values at one time

    r.set("count", 1)  # 1 value [set count value]

    r.incr("count")  # 2 value [increase by one at a time]

    r.incrby("count", 10)  # 12 value [increase by provided value]

    r.incrbyfloat("count", 2.5)  # increase value by float numbers

    print(f"redis result : {result}")


init()
