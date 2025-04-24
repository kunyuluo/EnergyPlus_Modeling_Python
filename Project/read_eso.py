import esoreader
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from matplotlib import pyplot as plt
from plotly.subplots import make_subplots

path = f'../Data/RefBldgs/YMCA_Singapore_test.eso'
dd, data = esoreader.read(path)
targets = dd.find_variable('Chiller Evaporator Cooling Rate')
# print(targets)
start = dt.datetime(2025, 1, 1, 0, 0, 0)
dti = pd.date_range(start=start, periods=52560, freq='10min')
df = pd.DataFrame(index=dti)
for i in range(len(targets)):
    frequency, key, variable = dd.find_variable('Chiller Evaporator Cooling Rate')[i]
    idx = dd.index[frequency, key, variable]
    time_series = data[idx]
    time_series = [power / 1000 for power in time_series]
    df[key] = time_series

start_date = dt.datetime(2025, 7, 28, 0, 0, 0)
end_date = dt.datetime(2025, 8, 4, 0, 0, 0)
df = df[(df.index >= start_date) & (df.index < end_date)]
print(df)

# fig = make_subplots(specs=[[{"secondary_y": True}]])
# fig.add_trace(go.Scatter(x=df.index, y=df['CHILLER 1'], mode='lines', name='CHILLER 1'))
# fig.add_trace(go.Scatter(x=df.index, y=df['CHILLER 2'], mode='lines', name='CHILLER 2'), secondary_y=False)
# fig.update_layout(title='YMCA Simulation', xaxis_title='Timestamp', yaxis_title='Cooling load (kW)', xaxis_tickangle=-45)
# fig.show()
