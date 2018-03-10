import redis

redis_server = redis.Redis("localhost")
redis_server.set("name", "Timothy")

print(redis_server.get("name"))
