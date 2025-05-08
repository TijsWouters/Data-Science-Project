import re
import sys
from tabulate import tabulate

def parse_tags(text):
    pattern = re.compile(r"<([^>]+)>\{([^}]+)\}")
    results = []
    cumulative_offset = 0

    def repl(match):
        nonlocal cumulative_offset

        orig_start = match.start()
        orig_end = match.end()

        adjusted_start = orig_start - cumulative_offset
        word = match.group(1)
        label = match.group(2)
        adjusted_end = adjusted_start + len(word)
        length = len(word.split())
        results.append((word, label, adjusted_start, adjusted_end, None, length))

        removed_length = (orig_end - orig_start) - len(word)
        cumulative_offset += removed_length
        return word

    cleaned_text = pattern.sub(repl, text)
    
    for i, result in enumerate(results):
        word, label, start, end, _, length = result
        word_index = len(cleaned_text[:start].split())
        results[i] = (word, label, start, end, word_index, length)
    
    return results, cleaned_text

def process_file(file_path):
    with open(file_path, encoding="utf-8") as f:
        text = f.read()
    results, cleaned_text = parse_tags(text)
    
    print("Extracted tags:")
    print(tabulate(results, headers=["Word", "Label", "Start", "End", "Index"], tablefmt="grid"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_labels.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    process_file(file_path)
