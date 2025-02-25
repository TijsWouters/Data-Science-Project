# Usage: python spacy-label.py <input_file> <output_file> [trained_pipeline]
# Input can be folder, then output will also be a folder
# You can install a trained pipeline using: python -m spacy download <pipeline>

import spacy
import sys
import os

nlp = None

def spacy_label(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
        
    text = "".join(lines)
        
    with open(output_file, 'w') as f:
        doc = nlp(text)
        for ent in sorted(doc.ents, key=lambda e: e.start_char, reverse=True):
            label = f" ({ent.label_})"
            text = text[:ent.end_char] + label + text[ent.end_char:]
        f.write(text)
            
def spacy_label_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file)
        output_file = os.path.join(output_folder, file)
        spacy_label(input_file, output_file)

if __name__ == "__main__":
    input_file, output_file = sys.argv[1], sys.argv[2]
    if (len(sys.argv) > 3):
        nlp = spacy.load(sys.argv[3])
    else:
        nlp = spacy.load("nl_core_news_lg")
    
    if (os.path.isdir(input_file)):
        spacy_label_folder(input_file, output_file)
    else:
        spacy_label(input_file, output_file)
    
    print(f"Named entities labeled in {input_file} and saved to {output_file}")