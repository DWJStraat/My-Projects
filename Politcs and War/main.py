import pnwkit
import json

config = json.load(open('config.json', 'r'))

kit = pnwkit.QueryKit(config['token'])

query = kit.query('nations',{'id':531131, 'first':1}, 'nation_name')

result = query.get()

print(f"nation name: {result.nations[0].nation_name}")
