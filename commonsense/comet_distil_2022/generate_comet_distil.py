from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import argparse
import json


# path to model directory
model_path = 'comet_distil_2022/downloaded/comet-distill-high/'
# Point to a file containing config.json, merges.txt, added_tokens.json, vocab.json, 
# special_tokens_map.json, tokenizer_config.json
#
# NOTE: you may have to rename tokenizer_config.json to config.json
tokenizer_path = 'comet_distil_2022/downloaded/comet-distill-tokenizer'


## load model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

'''

Generate an inference 

Requires: 
    Select an event, relation, and top_p if sampling (leaving it at 0. will 
    use greedy decoding)

'''

###Parser###
parser = argparse.ArgumentParser()
parser.add_argument("--device", type=int, default=0)
parser.add_argument("--model_path", type=str, default="comet_distil_2022/downloaded/comet-distill-high/")
parser.add_argument("--output_file", type=str, default="output.json")
parser.add_argument("--input", type=str, default="")
parser.add_argument("--sampling_algorithm", type=str, default="greedy")
    
args = parser.parse_args()

####
# Parameters
####

# input event to generate for
#event = 'Zero visibility in fog makes driving difficult'
event = args.input
# one of ['xEffect','xAttr','xReact', 'xWant','xIntent', 'xNeed', 'HinderedBy']
relation = 'xEffect'
# top_p
top_p = 0.5



####
# Generate, using parameters
####

inp_text = "<head> {} </head> <relation> {} </relation> [GEN] ".format(event.strip(),relation)
inp = tokenizer(inp_text)['input_ids']
tokens_out = model.generate(torch.tensor(inp).view(1,-1),top_p=top_p, do_sample=top_p > 0.).tolist()[0]
text_out = tokenizer.decode(tokens_out[len(inp):])

## trim to sentence end and/or newline
if '.' in text_out:
    text_out = text_out[:text_out.index('.')]
if '\n' in text_out:
    text_out = text_out[:text_out.index('\n')]

# finally, trim out only the inference
inference = text_out

####
# Print Result
####

print('INPUT:\n{}\n========'.format(inp_text))
print('INFERENCE:\n{}\n========'.format(inference))

json.dump(inference, open(args.output_file, "w"))