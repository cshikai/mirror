## EVAL ON MSMARCO

import json
import pandas as pd

def prec_at_k(corpus_ids, top_5, k):
    top_5 = [int(x) for x in top_5][:k]
    prec = len(set(top_5).intersection(corpus_ids))/len(top_5)
    return prec

def avg_prec_at_k(ground_truth, queries, k):
    cumulative_precision = 0

    for query in queries['queries']:
        corpus_ids = ground_truth[ground_truth['query-id'] == query['id']]['corpus-id']
        precision = prec_at_k(corpus_ids, query['top_5'], k)
        cumulative_precision += precision

    ave_precision = cumulative_precision/len(queries['queries'])

    return ave_precision

def hits_at_k(corpus_ids, top_5, k):
    top_5 = [int(x) for x in top_5]
    if len(set(top_5[:k]).intersection(corpus_ids)):
        return 1
    else:
        return 0

def avg_hits_at_k(ground_truth, queries, k):
    cumulative_hits_at_k = 0
    for query in queries['queries']:
        corpus_ids = ground_truth[ground_truth['query-id'] == query['id']]['corpus-id']
        cumulative_hits_at_k += hits_at_k(corpus_ids, query['top_5'], k)

    avg_hits_at_k = cumulative_hits_at_k/len(queries['queries'])

    return avg_hits_at_k



if __name__ == "__main__":
    result_dir = './test_result.json'
    g_truth_dir = './test.tsv'

    ground_truth = pd.read_table(g_truth_dir)

    ground_truth = ground_truth[ground_truth['score'] != 0]
    # print(ground_truth.head())

    with open(result_dir, 'r') as f:
        result = json.load(f)

    avg_prec_1 = avg_prec_at_k(ground_truth, result, 1)
    avg_prec_3 = avg_prec_at_k(ground_truth, result, 3)
    avg_prec_5 = avg_prec_at_k(ground_truth, result, 5)
    print("Avg precision at 1, 3, 5: {}; {}; {}".format(avg_prec_1, avg_prec_3, avg_prec_5))
    avg_hits_1 = avg_hits_at_k(ground_truth, result, 1)
    avg_hits_3 = avg_hits_at_k(ground_truth, result, 3)
    avg_hits_5 = avg_hits_at_k(ground_truth, result, 5)
    print("Avg hits at 1, 3, 5: {}; {}; {}".format(avg_hits_1, avg_hits_3, avg_hits_5))
