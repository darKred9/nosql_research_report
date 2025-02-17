import altair as alt
import pandas as pd
import numpy as np
import time
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["benchmark"]
collection = db["test"]

# batch sizes
batch_sizes = list(range(500, 60001, 2000))
num_records = 100000
results = []

for batch_size in batch_sizes:
    collection.delete_many({}) 

    start_time = time.time()

    for _ in range(num_records // batch_size):
        batch = [{"value": "a" * 1024} for _ in range(batch_size)]
        collection.insert_many(batch)

    end_time = time.time()
    total_time = end_time - start_time
    tps = num_records / total_time

    results.append({"Batch Size": batch_size, "TPS": tps})

df = pd.DataFrame(results)

client.close()

chart = alt.Chart(df).mark_line().encode(
    x=alt.X("Batch Size", title="Batch Size"),
    y=alt.Y("TPS", title="Transactions Per Second (TPS)"),
    tooltip=["Batch Size", "TPS"]
).properties(
    title="MongoDB TPS vs. Batch Size"
)

chart.save('cc.html')

