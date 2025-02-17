import altair as alt
import pandas as pd

data = pd.DataFrame({
    "Database": ["MongoDB", "Redis"],
    "TPS": [1927.16, 44130],
    "Latency (ms)": [0.52, 0.02]
})

bar_tps = alt.Chart(data).mark_bar().encode(
    x=alt.X("Database", title="Database"),
    y=alt.Y("TPS", title="Transactions Per Second (TPS)"),
    color="Database"
).properties(
    title="MongoDB vs Redis: Write TPS"
)

dot_latency = alt.Chart(data).mark_circle(size=200).encode(
    x=alt.X("Database", title="Database"),
    y=alt.Y("Latency (ms)", title="Average Latency (ms)", scale=alt.Scale(type="log")),
    color="Database"
).properties(
    title="MongoDB vs Redis: Write Latency"
)

(bar_tps | dot_latency).save("write_chart.html")
print("write_chart.html - generated!")
