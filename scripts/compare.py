import sys
import os

from anonymize import Annotation
from extract_labels import parse_tags
from labelmapping import VALID_TAGS

def annotations_from_file(file_name):
    with open(file_name, 'r') as f:
        text = f.read()
        
    annotations = []
        
    tags, cleaned_text = parse_tags(text)
    for result in tags:
        if result[1] not in VALID_TAGS:
            raise ValueError(f"Invalid tag: {result[1]} in file: {file_name}")
        annotations.append(Annotation(
            result[0],  # word
            result[1],  # label
            result[2],  # start
            result[3]   # end
        ))
    return annotations, cleaned_text    
        
def get_annotations_for_methods(labeled_folder):
    prev_cleaned_text = None
    prev_method = None
    annotations = {}
    
    methods = os.listdir(labeled_folder)
    methods.remove("truth")
    methods.insert(0, "truth")
    file_names = os.listdir(labeled_folder + "/truth")
    
    for file_name in file_names:
        if not file_name.endswith(".txt"):
            continue
        
        prev_cleaned_text = None
        prev_method = None
        
        annotations[file_name] = {}
        
        for method in methods:
            if method == "nltk": continue
            annotations[file_name][method], cleaned_text = annotations_from_file(labeled_folder + "/" + method + "/" + file_name)
            if prev_cleaned_text is not None and cleaned_text != prev_cleaned_text:
                diff_context(prev_cleaned_text, cleaned_text)
                raise ValueError(f"Mismatch in cleaned text for file: {file_name} between {method} and {prev_method}")
                
            
        prev_cleaned_text = cleaned_text
        prev_method = method
            
                
                
    return annotations
            
import difflib

# Check if strings are equal, if not print the context around the difference
def diff_context(s1, s2, context=3):
    if s1 == s2:
        return

    words1 = s1.split()
    words2 = s2.split()
    
    sm = difflib.SequenceMatcher(None, words1, words2)
    opcodes = sm.get_opcodes()

    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            continue
        
        start1 = max(i1 - context, 0)
        end1 = min(i2 + context, len(words1))

        start2 = max(j1 - context, 0)
        end2 = min(j2 + context, len(words2))
        
        context_str1 = " ".join(words1[start1:end1])
        context_str2 = " ".join(words2[start2:end2])
        
        print("Difference found:")
        print("String 1 context: ...", context_str1, "...")
        print("String 2 context: ...", context_str2, "...")
        print("-" * 40)

def strict_match(a, b):
    return a == b

def pos_match(a, b):
    return a.start == b.start and a.end == b.end

def larger_match(a, b):
    return a.start <= b.start and a.end >= b.end


def compute_results(annotations, compare_function=strict_match):    
    results = {}
    
    file_names = os.listdir(labeled_folder + "/truth")
    methods = os.listdir(labeled_folder)
    
    for method in methods:
        if method == "nltk": continue
        results[method] = {
            'TP': 0,
            'FP': 0,
            'FN': 0,
        }
        for file_name in file_names:
            if (file_name in ["KNMP2013def-QuickTime.txt", "KNMP2014-2-def2MP4.txt", "KNMP2015-farmagenetica.txt"]):
                continue
            #print(f"\nProcessing {file_name} for method {method}\n")
            truth_annotations = annotations[file_name]['truth']
            method_annotations = annotations[file_name][method]
            
            for truth_annotation in truth_annotations:
                matched = False
                for method_annotation in method_annotations:
                    if compare_function(truth_annotation, method_annotation):
                        matched = True
                        results[method]['TP'] += 1
                        break
                if not matched:
                    #print(f"False negative: {truth_annotation} in {file_name} for method {method}")
                    results[method]['FN'] += 1

            for method_annotation in method_annotations:
                matched = False
                for truth_annotation in truth_annotations:
                    if compare_function(truth_annotation, method_annotation):
                        matched = True
                        break
                if not matched:
                    #print(f"False positive: {method_annotation} in {file_name} for method {method}")
                    results[method]['FP'] += 1
            
    return results

from tabulate import tabulate

def print_tabulated_results(results):
    tabulated_results = []
    headers = ["Method", "TP", "FP", "FN", "Precision", "Recall", "F1"]
    
    for method, result in results.items():
        precision = result['TP'] / (result['TP'] + result['FP']) if (result['TP'] + result['FP']) > 0 else 0
        recall = result['TP'] / (result['TP'] + result['FN']) if (result['TP'] + result['FN']) > 0 else 0
        f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        tabulated_results.append([method, result['TP'], result['FP'], result['FN'], precision, recall, f1_score]) 
    print(tabulate(tabulated_results, headers=headers, tablefmt="github"))   
        


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
    print("Strict match results:")    
    print_tabulated_results(results)
    
    print("POS match results:")
    results = compute_results(annotations, pos_match)
    print_tabulated_results(results)
    
    print("Larger match results:")
    results = compute_results(annotations, larger_match)
    print_tabulated_results(results)
