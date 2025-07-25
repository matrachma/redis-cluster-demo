# python-app/app.py
import time
import random
from redis.cluster import RedisCluster
from redis.exceptions import ConnectionError, ClusterDownError

# Define a fixed list of 16 keys
REDIS_KEYS = [f"user:session:{i}" for i in range(1, 17)]

if __name__ == '__main__':
    # Add a small delay to allow the cluster to initialize
    time.sleep(15)
    
    while True:
        try:
            print("Attempting to connect to Redis Cluster...")
            
            # Point to just one node. The client will discover the rest.
            rc = RedisCluster(host="redis-1", port=6379, decode_responses=True)
            
            print("✅ Python App: Successfully connected to Redis Cluster.")
            
            counter = 0
            while True:
                try:
                    # Cycle through the predefined list of keys
                    key_to_use = REDIS_KEYS[counter % len(REDIS_KEYS)]
                    
                    # The value can still be dynamic
                    value_to_set = f"data-{random.randint(1000, 9999)}"
                    
                    rc.set(key_to_use, value_to_set)
                    value = rc.get(key_to_use)
                    print(f"[{time.strftime('%H:%M:%S')}] Python App: SET {key_to_use} to {value}")
                    
                    counter += 1
                    time.sleep(1.5)
                except (ConnectionError, ClusterDownError) as e:
                    print(f"🔴 Python App: Connection lost: {e}. Reconnecting...")
                    break
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    time.sleep(5)

        except Exception as e:
            print(f"🔴 Python App: Could not connect to Redis Cluster: {e}. Retrying...")
            time.sleep(5)
