import pandas as pd
import json

with open('C:/Users/xalba/Desktop/data2.json') as f:
  data = json.load(f)
  
    df=pd.DataFrame.from_dict(data, orient='index')
    
    df.T.plot()