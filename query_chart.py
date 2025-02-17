import altair as alt
import pandas as pd

data = {
    'Database': ['MongoDB', 'Redis', 'MongoDB', 'Redis', 'MongoDB', 'Redis'],
    'Test Type': ['Single Query', 'Single Query', 'Batch Query', 'Batch Query', 'Concurrent Query', 'Concurrent Query'],
    'Latency (ms)': [0.63, 0.11, 1.88, 0.79, 0.47, 0.15] ## test data
}

df = pd.DataFrame(data)

grouped_bar = alt.Chart(df).mark_bar().encode(
    x=alt.X('Test Type:N', title='Type'),
    y=alt.Y('Latency (ms):Q', title='Latency (mm)'),
    color=alt.Color('Database:N', title='Database'),
    xOffset='Database:N'
).properties(
    width=400,
    height=300,
    title='MongoDB vs Redis: Query Performance'
)

grouped_bar.save('query_chart.html')
print("query_chart.html - generated!")

