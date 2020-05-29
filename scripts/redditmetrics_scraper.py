import demjson
import requests
import pandas as pd

r = requests.get('http://www.redditmetrics.com/r/bitcoin')

json_data = r.text.split('data: ')[1].split('pointSize')[0].strip()[:-1].replace('\n', '')
growth = demjson.decode(json_data)
growth_df = pd.DataFrame(growth)
growth_df.columns = ['date', 'growth']
growth_df.to_csv("btc_growth.csv")

json_data = r.text.split('data: ')[2].split('pointSize')[0].strip()[:-1].replace('\n', '')
total = demjson.decode(json_data)
total_df = pd.DataFrame(total)
total_df.columns = ['date', 'total']
total_df.to_csv("btc_total.csv")


r = requests.get('http://www.redditmetrics.com/r/litecoin')

json_data = r.text.split('data: ')[1].split('pointSize')[0].strip()[:-1].replace('\n', '')
growth = demjson.decode(json_data)
growth_df = pd.DataFrame(growth)
growth_df.columns = ['date', 'growth']
growth_df.to_csv("ltc_growth.csv")

json_data = r.text.split('data: ')[2].split('pointSize')[0].strip()[:-1].replace('\n', '')
total = demjson.decode(json_data)
total_df = pd.DataFrame(total)
total_df.columns = ['date', 'total']
total_df.to_csv("ltc_total.csv")

r = requests.get('http://www.redditmetrics.com/r/ethereum')

json_data = r.text.split('data: ')[1].split('pointSize')[0].strip()[:-1].replace('\n', '')
growth = demjson.decode(json_data)
growth_df = pd.DataFrame(growth)
growth_df.columns = ['date', 'growth']
growth_df.to_csv("eth_growth.csv")

json_data = r.text.split('data: ')[2].split('pointSize')[0].strip()[:-1].replace('\n', '')
total = demjson.decode(json_data)
total_df = pd.DataFrame(total)
total_df.columns = ['date', 'total']
total_df.to_csv("eth_total.csv")
