import json

FILE_PATH = "mashqa_data/train_webmd_squad_v2_full.json"
OUT_PATH = "train_full.json"
with open(FILE_PATH, 'r') as json_file:
    data = json.load(json_file)

QUERY_SEPARATOR = "<CLS>"
ANS_START = "<ANSSTART>"
ANS_END = "<ANSEND>"

data = data['data']
input = []
output = []
mx_len = 0
for dt in data:
    for paragraph in dt['paragraphs']:
        for qa in paragraph['qas']:
            input.append(qa['question'] + QUERY_SEPARATOR + paragraph['context'])
            mx_len = max(mx_len, len(input[-1]))
            ans = ""
            assert(len(qa['answers']) == 1) # passed for train_full
            for idx, sent in enumerate(paragraph['sent_list']):
                if idx in qa['answers'][0]['answer_span']:
                    ans += ANS_START +  sent + ANS_END
                else:
                    ans += sent
            output.append(ans)
            mx_len = max(mx_len, len(output[-1]))

        
out = {
    'input' : input,
    'output' : output
}

with open(OUT_PATH, 'w') as file:
    json.dump(out, file)

print(mx_len)
                    