# A Redis stream is a data structure that acts like an append-only log but also implements several operations to overcome some of the limits of a typical append-only log.
# You can use streams to record and simultaneously syndicate events in real time. Examples of Redis stream use cases include:
# ---- Event sourcing (e.g., tracking user actions, clicks, etc.)
# ---- Sensor monitoring (e.g., readings from devices in the field)
# ---- Notifications (e.g., storing a record of each user's notifications in a separate stream)
# *** Basic commands
# -- XADD adds a new entry to a stream.
# --XREAD reads one or more entries, starting at a given position and moving forward in time.
# --XRANGE returns a range of entries between two supplied entry IDs.
# --XLEN returns the length of a stream.
# --XDEL removes entries from a stream.
# --XTRIM trims a stream by removing older entries.

import redis

rds = redis.Redis(port=6379, host="localhost", db=0)


def stream_init():
    rds.xadd("notify", {"msg": 4, "friend_req": 34})  # add new entry to stream.
    rds.xdelex("notify", "msg")  # delete one or multiple entries from strem.
    rds.xlen("notify")  # return the length of a stream
