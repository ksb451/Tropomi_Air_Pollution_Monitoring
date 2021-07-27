import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data_val.csv", index_col=0)
print(df.head())
df.info()
df.index = pd.to_datetime(df.index)
df.info()
print(df.head())

fig, ax = plt.subplots(figsize=(20, 10))
ax.scatter(df.index.values,
        df['0'],
        color='purple')
ax.plot(df.index.values,
        df['0'],
        color='purple')
ax.set(xlabel="Date",
       ylabel="CO Tropospheric Column (mol/m2)",
       title="CO level in Delhi as per the last few years")
plt.setp(ax.get_xticklabels(), rotation=45)

plt.show()
