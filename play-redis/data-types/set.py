import redis

rds = redis.Redis(host="localhost", port=6379, db=0)


def setInit():
    rds.sadd(
        "numbers", "1", "2", "3", "4", "5", "4", "3"
    )  # add unique values only not duplicacy.
    rds.srem("numbers", "2")  # remove the specific value from the set .
    rds.sismember("numbers", "3")  # check if specific value is part of the set or not.
    rds.spop("numbers")  # remove and return  the random member of set.
    rds.scard("numbers")  # return the number of elements in a set.
    rds.smembers("numbers")  # return all element in a set.
    rds.sinter(
        "numbers", "numbers-2"
    )  # return the member of set that intersects in two or more sets.
    rds.smove(
        "numbers", "numbers-2", "3"
    )  # move element three from [numbers] set to [numbers-2] set.
    rds.srandmember("numbers")  # get one or multiple random member from set.


setInit()
