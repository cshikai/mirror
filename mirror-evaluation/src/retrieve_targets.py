import json
import pandas as pd

data_dir = './queries.jsonl'
test_dir = './dev.tsv'
json_out = './dev_pairs.json'
data = pd.read_json(data_dir, lines=True)

test = pd.read_table(test_dir)

print(data.head())
print(test.head())

query_ids = test['query-id']
query_ids = list(set(query_ids))

query_list = []
#
for query_id in query_ids:
    id = query_id
    row = data.loc[data['_id']== id]
    text = row.iloc[0]['text']
    pairs = {'id': id, 'text': text}
    query_list.append(pairs)

# print(query_list[:10])

Dictionary = {'data':query_list}

with open(json_out, 'w') as f:
    json.dump(Dictionary, f, indent=2)

# with open(json_out, 'r') as f:
#     x = json.load(f)
#
# print(x['data'][:3])