import sys
import os

from anonymize import Annotation
from extract_labels import parse_tags
from tagmapping import VALID_TAGS

def annotations_from_file(file_name):
    with open(file_name, 'r') as f:
        text = f.read()
        
    annotations = []
        
    tags, cleaned_text = parse_tags(text)
    for result in tags:
        if result[2] not in VALID_TAGS:
            raise ValueError(f"Invalid tag: {result.tag()}")
        annotations.append(Annotation(
            result[0],  # word
            result[1],  # label
            result[2],  # start
            result[3]   # end
        ))
    return annotations, cleaned_text    
        
def get_annotations_for_methods(labeled_folder):
    prev_cleaned_text = None
    prev_file_name = None
    annotations = []
    # read folders in labeled_folder
    for method in os.listdir(labeled_folder):
        annotations[method] = []
        folder_path = os.path.join(labeled_folder, method)
        if not os.path.isdir(folder_path):
            continue
        
        # read files in folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if not file_name.endswith('.txt'):
                continue
            
            # read annotations from file
            annotations_for_file, cleaned_text = annotations_from_file(file_path)
            # check if cleaned_text is the same as previous
            if cleaned_text and cleaned_text != prev_cleaned_text:
                raise ValueError(f"Cleaned text mismatch in file: {file_name} and {prev_file_name}")
            annotations[method][file_name] = annotations_for_file
            prev_cleaned_text = cleaned_text
            prev_file_name = file_name
    return annotations


def compute_results(annotations):
    truth_annotations = annotations['truth']
    
    results = []
    
    for method, method_annotations in annotations.items():
        results[method] = {
            'TP': 0,
            'FP': 0,
            'FN': 0,
        }
        if (method == 'truth'):
            continue
        for annotation in method_annotations:
            if annotation in truth_annotations:
                results[method]['TP'] += 1
            else:
                results[method]['FP'] += 1
        for annotation in truth_annotations:
            if annotation not in method_annotations:
                results[method]['FN'] += 1
    return results


if __name__ == "__main__":
    # usage python compare.py <labeled_folder>
    if (len(sys.argv) != 2):
        print("Usage: python compare.py <labeled_folder>")
        sys.exit(1)
        
    labeled_folder = sys.argv[1]
    if not os.path.isdir(labeled_folder):
        print(f"Invalid folder: {labeled_folder}")
        sys.exit(1)
    annotations = get_annotations_for_methods(labeled_folder)
    results = compute_results(annotations)
    for method, result in results.items():
        print(f"Method: {method}")
        print(f"TP: {result['TP']}")
        print(f"FP: {result['FP']}")
        print(f"FN: {result['FN']}")
        print(f"Precision: {result['TP'] / (result['TP'] + result['FP'])}")
        print(f"Recall: {result['TP'] / (result['TP'] + result['FN'])}")
        print(f"F1: {2 * result['TP'] / (2 * result['TP'] + result['FP'] + result['FN'])}")
        print()