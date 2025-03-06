# Usage: python spacy-label.py <anonymize|label> <input_file> <output_file> [trained_pipeline]
# Input can be folder, then output will also be a folder
# You can install a trained pipeline using: python -m spacy download <pipeline>

import spacy
import sys
import os

nlp = None

def spacy_label(input_file, output_file, anonymize=False):
    with open(input_file, 'r') as f:
        lines = f.readlines()
        
    text = "".join(lines)
        
    with open(output_file, 'w') as f:
        doc = nlp(text)
        for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
            if anonymize:
                if ent.label_ in ['DATE', 'FAC', 'GPE', 'ORG', 'PERSON', 'TIME', 'NORP']:
                    label = f"({ent.label_})"
                    text_list = list(text)
                    text_list[ent.start_char:ent.end_char] = list(label)
                    text = "".join(text_list)
            else:
                label = f" ({ent.label_})"
                text = text[:ent.end_char] + label + text[ent.end_char:]
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
        nlp = spacy.load(sys.argv[4])
    else:
        nlp = spacy.load("nl_core_news_lg")
    
    if (os.path.isdir(input_file)):
        spacy_label_folder(input_file, output_file, anonymize)
    else:
        spacy_label(input_file, output_file, anonymize)
    
    print(f"Named entities labeled in {input_file} and saved to {output_file}")