import json
from sample_dylib import BertModel
import sys
# import numpy as np
import math
mode = ''
context_path = ''
if len(sys.argv) > 2:
    mode = sys.argv[2]
    model_path = sys.argv[1]
elif len(sys.argv) > 1:
    model_path = sys.argv[1]
else:
    print("Usage: python3 sample_dylib.py <ggml model path>")
    exit(0)

def argsort(arr):
    return sorted(range(len(arr)), key=lambda i: arr[i])

def dot_product(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have the same dimension for dot product")

    result = sum(x * y for x, y in zip(vector1, vector2))
    return result

def euclidean_norm(vector):
    squared_sum = sum(x**2 for x in vector)
    result = math.sqrt(squared_sum)
    # print(vector)
    return result + 0.1

FILE_PATH = "test/movies/train_webmd_squad_v2_full.json"
OUT_PATH = "train_full_chunked.json"
with open(FILE_PATH, 'r') as json_file:
    data = json.load(json_file)

data = data['data']
# input = []
# output = []
mx_len = 0
MAX_LEN = 5000

model = BertModel(model_path)

# print(f"Loaded {len(texts)} lines.")

def print_results(res):
    closest_texts = res
    # Print the closest texts and their similarity scores
    print("Closest texts:")
    for i, text in enumerate(closest_texts):
        print(f"{i+1}. {text})")

# Define the function to query the k closest texts
def query(texts, embedded_texts, text, k=3, threshold=0.5):
    # Embed the input text
    embedded_text = model.encode(text)
    # print(embedded_text)
    # Compute the cosine similarity between the input text and all the embedded texts
    similarities = [dot_product(embedded_text, embedded_text_i) / (euclidean_norm(embedded_text) * euclidean_norm(embedded_text_i)) for embedded_text_i in embedded_texts]
    # Sort the similarities in descending order
    sorted_indices = argsort(similarities)[::-1]
    # Return the k closest texts and their similarities
    closest_texts = [texts[i] for i in sorted_indices if similarities[i] > threshold]
    closest_similarities = [similarities[i] for i in sorted_indices if similarities[i] > threshold]
    return closest_texts

if mode == 'train_data':
    limit = 1
    for dt in data[:2]:
        for paragraph in dt['paragraphs'][:limit]:
            embedded_texts = model.encode(paragraph['sent_list'])
            for qa in paragraph['qas']:
                assert(len(qa['answers']) == 1) # passed for train_full
                # input.append(qa['question'] + QUERY_SEPARATOR + paragraph['context'])

                pred = query(paragraph['sent_list'],embedded_texts,qa['question'])
                print(qa['question'])
                print_results(pred[:5])
                ytrue = []
                for idx, sent in enumerate(qa['answers'][0]['answer_span']):
                    ytrue.append(paragraph['sent_list'][sent])
                # print(ytrue)
                # ytrue = sorted(ytrue)
                # pred = sorted(pred)
                # scores = [np.dot(embedded_text, embedded_text_i) / (np.linalg.norm(embedded_text) * np.linalg.norm(embedded_text_i)) for embedded_text_i in embedded_texts]
elif mode == "context_input":
    context = input("Enter context (separate sentences with ;): ")
    context = context.split(';')
    embedded_context = model.encode(context)
    inp = input("Enter query(q to exit): ")
    while inp != "q":
        pred = query(context, embedded_context, inp)
        print_results(pred)
        inp = input("Enter query(q to exit): ")
elif mode == "context_file":
    with open(sys.argv[3], "r") as f:
        texts = f.readlines()
    embedded_texts = model.encode(texts)
    inp = input("Enter query(q to exit): ")
    while inp != "q":
        pred = query(texts, embedded_texts, inp)
        print_results(pred)
        inp = input("Enter query(q to exit): ")

print(mx_len)

            