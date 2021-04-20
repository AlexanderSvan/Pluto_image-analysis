import pandas as pd
import json
import matplotlib.pyplot as plt

with open('C:/Users/xalba/Desktop/data2.json') as f:
  data = json.load(f)
  
df=pd.DataFrame.from_dict(data, orient='index')

df.T.plot()
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))