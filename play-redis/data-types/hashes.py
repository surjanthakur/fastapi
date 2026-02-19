import redis

rds = redis.Redis(host="localhost", port=6379, db=0)


def hashesInit():
    rds.hset(
        "students",
        mapping={
            "name": "surjan",
            "age": 20,
            "rollno": 112,
            "city": "delhi",
            "country": "india",
        },
    )  # set the hash student record with its values.
    rds.hget("students", "name")  # get the name from student record.
    rds.hgetall("students")  # return all fields and values from record.
    rds.hmget(
        "students", "name", "city", "age"
    )  # get multiple values at one time from record.
    rds.hexists("students", "name")  # check if field exist in record or not.

    rds.delete(
        "students", "name", "age"
    )  # delete one or more fields and values from record if no fields left it deletes the hash record.
    rds.hgetdel(
        "students", "name"
    )  # delete the name fiels,value and return the value of deleted ones.

    rds.hlen("students")  # return the numbers of fields in record
    rds.hstrlen("sturents", "name")  # return the length of the values.
    rds.hvals("students")  # return the list of values in a hash record.
    rds.hrandfield("students")  # return one or more randome fields from hash record.
    rds.incrby("students", "age", 2)  # it increases the students age by 2 [20+2 = 22]


hashesInit()
