import json
import requests
import pandas as pd


"""Setting the headers to send and accept json responses
"""
header = {'Content-Type': 'application/json', \
                  'Accept': 'application/json'}

"""Reading test batch
"""
#df = pd.read_csv(utils.path+'/data/test.csv', encoding="utf-8-sig")
#df = df.head()

"""Converting Pandas Dataframe to json
"""

data = {
    "id": "19826478126",
    "x_1": 1.0,
    "x_2": -0.414120,
    "x_3": 0.2131,
    "x_4": -1.2}

#data = df.to_json(orient='records')

#print(data)


"""POST <url>/predict
"""
resp = requests.post("http://0.0.0.0:8080/v0/predict", \
                    data = json.dumps(data),\
                    headers= header)

print("STATUS-------------")
print(resp.status_code)


"""The final response we get is as follows:
"""
print("===== PREDICTIONS ===")
print(resp.json())