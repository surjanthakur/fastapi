import redis

rds = redis.Redis(host="localhost", port=6379, db=0)


def listinit():
    rds.lpush("msg", "hey")
    rds.lpush("msg", "holla")
    rds.lpush("msg", "namaste")  # push values in left side.
    rds.lpop("msg")  # pop the value from the head of the list.
    rds.rpush("msg", "holla")  # push the value in right side.
    rds.rpop("msg")  # pop the value from the  right side.

    rds.delete("msg")  # delete the list.
    rds.llen("msg")  # get the length of the list.
    rds.lrange("msg", 0, 2)  # get values from 0 index to 2 index
    rds.lrange("msg", 0, -1)  # from start to end list values
    rds.lmove(
        "msg", "another-msg", "right", "left"
    )  # now the right side value in [msg] move to left side in [another-msg]

    rds.blpop("msg")  # remove and return an element from head of list
    rds.blpop(
        "msg", 10
    )  # first we remove all values now the list is nill so now it wait the 10 second.
    # if: a values comes it remove and return the value else: comand block it wait for 10 second timeperiod until a new element becomes available.
    rds.blmove(
        "msg", "another-msg", 30
    )  # atomically moves elements from a [msg] list to a [another-msg] list.
    # If the source list is empty, the command will block until a new element becomes available.


listinit()
