# Usage: python deidentify-label.py <anonymize|label> <input_file> <output_file> [model]
# Input can be folder, then output will also be a folder
# You can install a trained pipeline using: python -m spacy download <pipeline>

from deidentify.base import Document
from deidentify.tokenizer import TokenizerFactory
from deidentify.taggers import FlairTagger
from deidentify.util import mask_annotations
import sys
import os

model = 'model_bilstmcrf_ons_fast-v0.2.0'
anonymize = False

tokenizer = None
tagger = None

def spacy_label(input_file, output_file, anonymize=False):
    with open(input_file, 'r') as f:
        lines = f.readlines()
        
    text = "".join(lines)
        
    with open(output_file, 'w') as f:
        docs = [Document(name='test', text=text)]
        
        annotations = tagger.annotate(docs)
        
        print(annotations[0].annotations)
        
        if anonymize:
            text = mask_annotations(annotations[0]).text
        else:
            for ent in sorted(annotations[0].annotations, key=lambda e: e.start, reverse=True):
                label = f" ({ent.tag})"
                text = text[:ent.end] + label + text[ent.end:]
        f.write(text)
            
def spacy_label_folder(input_folder, output_folder, anonymize=False):
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file)
        output_file = os.path.join(output_folder, file)
        spacy_label(input_file, output_file, anonymize)

if __name__ == "__main__":
    anonymize_option, input_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]
    if (anonymize_option.lower() == "anonymize"):
        anonymize = True
    if (len(sys.argv) > 4):
        model = sys.argv[4]
        
    tokenizer = TokenizerFactory().tokenizer(corpus='ons', disable=("tagger", "ner"))
    tagger = FlairTagger(model=model, tokenizer=tokenizer, verbose=False)
    print(model)
    
    if (os.path.isdir(input_file)):
        spacy_label_folder(input_file, output_file, anonymize)
    else:
        spacy_label(input_file, output_file, anonymize)
    
    print(f"Named entities labeled in {input_file} and saved to {output_file}")