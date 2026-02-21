import redis


rds = redis.Redis(port=6379, host="localhost", db=0)


def sorted_init():
    rds.zadd(
        "players", {"roy": 20, "aman": 45, "ashi": 5, "gill": 3}
    )  #!  to add values in sorted set
    rds.zrange("players", 0, -1)  # * get members accourding to range [asc] order.
    rds.zrevrange("players", 0 - 1)  # * get members accounrding to range reverse order.
    rds.zrem("players", "aman")  # * remove the values
    rds.zscore("players", "roy")  # * get the score of a member
    rds.zrank("players", "roy")  # * return the member index from sorted_set [0]
    rds.zpopmax(
        "players"
    )  # * return and delete the maximum score member from [sorted_set].
    # if the set last value is poped it removes the set
    rds.zpopmin(
        "players"
    )  # * return and delete the lowest score member from [sorted_set].
    # delete the sorted_set if last member poped
    rds.zrandmember("players")  # return one or more  random member from sorted_set.


sorted_init()
