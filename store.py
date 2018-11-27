import redis
def store_number(data):

    conn = redis.from_url('redis://localhost:6379')
    conn.zadd(data['user'],
              data['value'],
              data['timestamp'])

