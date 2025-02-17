import time
import random
from pymongo import MongoClient
import redis
from concurrent.futures import ThreadPoolExecutor

class DatabaseBenchmark:
    def __init__(self):
        self.mongo_client = MongoClient('mongodb://localhost:27017/')
        self.mongo_db = self.mongo_client['benchmark2']
        self.mongo_collection = self.mongo_db['test']
        
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        
        self.num_records = 100000
        
    def setup(self):
        self.mongo_collection.drop()
        self.redis_client.flushdb()
        
        test_data = []
        for i in range(self.num_records):
            key = f"key_{i}"
            value = "a" * 1000  # 1KB data filled with 'a'
            test_data.append({"_id": key, "value": value})    
            self.redis_client.set(key, value) # insert the data into redis
        
        self.mongo_collection.insert_many(test_data) # insert the data into mongodb
    
    def test_single_read(self, num_queries=10000):
        print("\n Single Query Test...")
        
        # MongoDB
        start_time = time.time()
        for _ in range(num_queries):
            key = f"key_{random.randint(0, self.num_records-1)}"
            self.mongo_collection.find_one({"_id": key})
        mongo_time = time.time() - start_time
        
        # Redis
        start_time = time.time()
        for _ in range(num_queries):
            key = f"key_{random.randint(0, self.num_records-1)}"
            self.redis_client.get(key)
        redis_time = time.time() - start_time
        
        print(f"MongoDB AVG Latency: {(mongo_time/num_queries)*1000:.2f} ms")
        print(f"Redis AVG Latency: {(redis_time/num_queries)*1000:.2f} ms")
        
    def test_batch_read(self, batch_size=100, num_batches=100):
        print("\nBatch Query Test...")
        
        # MongoDB
        start_time = time.time()
        for _ in range(num_batches):
            keys = [f"key_{random.randint(0, self.num_records-1)}" for _ in range(batch_size)]
            list(self.mongo_collection.find({"_id": {"$in": keys}}))
        mongo_time = time.time() - start_time
        
        # Redis
        start_time = time.time()
        for _ in range(num_batches):
            keys = [f"key_{random.randint(0, self.num_records-1)}" for _ in range(batch_size)]
            self.redis_client.mget(keys)
        redis_time = time.time() - start_time
        
        print(f"Batch Size: {batch_size}")
        print(f"MongoDB AVG Latency: {(mongo_time/num_batches)*1000:.2f} ms")
        print(f"Redis AVG Latency: {(redis_time/num_batches)*1000:.2f} ms")
    
    def test_concurrent_read(self, num_threads=10, queries_per_thread=1000):
        print("\nConcurrent Query Test...")
        
        def mongo_worker():
            for _ in range(queries_per_thread):
                key = f"key_{random.randint(0, self.num_records-1)}"
                self.mongo_collection.find_one({"_id": key})
        
        def redis_worker():
            for _ in range(queries_per_thread):
                key = f"key_{random.randint(0, self.num_records-1)}"
                self.redis_client.get(key)
        
        # MongoDB
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(mongo_worker) for _ in range(num_threads)]
            for future in futures:
                future.result()
        mongo_time = time.time() - start_time
        
        # Redis
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(redis_worker) for _ in range(num_threads)]
            for future in futures:
                future.result()
        redis_time = time.time() - start_time
        
        total_queries = num_threads * queries_per_thread

        print(f"Number of Threads: {num_threads}")
        print(f"MongoDB AVG Latency: {(mongo_time/total_queries)*1000:.2f} ms")
        print(f"Redis AVG Latency: {(redis_time/total_queries)*1000:.2f} ms")
    
    def run_all_tests(self):
        self.setup()
        self.test_single_read()
        self.test_batch_read()
        self.test_concurrent_read()
        
        self.mongo_client.close()
        self.redis_client.close()

if __name__ == "__main__":
    benchmark = DatabaseBenchmark()
    benchmark.run_all_tests()



