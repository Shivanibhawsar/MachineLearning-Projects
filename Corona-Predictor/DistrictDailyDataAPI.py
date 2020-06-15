import requests
import json
import pandas as pd
import os



def fetchLatestData():
    response = requests.get('https://api.covid19india.org/districts_daily.json')
    content = response.content
    parsed = json.loads(content)
    columnList = ['state','district','active','confirmed','deceased','recovered','date']
    dfs = pd.DataFrame(columns = columnList)
    r = json.dumps(parsed['districtsDaily'])
    loaded_r = json.loads(r)
    for i in loaded_r:
        state_name = loaded_r[i]
        df = []
        r = json.dumps(loaded_r[i])
        loaded_d = json.loads(r)
        for j in loaded_d:
            district_name = loaded_d[j]
            r = json.dumps(loaded_d[j])
            loaded_v = json.loads(r)
            for k in loaded_v:
                df.append(i)
                df.append(j)
                active = k['active']
                confirmed = k['confirmed']
                deceased = k['deceased']
                recovered = k['recovered']
                date = k['date']
                df.append(active)
                df.append(confirmed)
                df.append(deceased)
                df.append(recovered)
                df.append(date)
                dfs = dfs.append(pd.Series(df, index=columnList), ignore_index=True)
                df = []
    print(os.getcwd() +'/assets/'+'India_district_daily.csv');
    dfs.to_csv(os.getcwd() +'/assets/'+'India_district_daily.csv', index=False)






