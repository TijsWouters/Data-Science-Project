import re
import sys
import os

from numbers_to_digits import numbers_to_digits

def remove_time_annotations(text):
    lines = text.split('\n')
    
    new_lines = []
    for line in lines:
        if not re.match('.*\[(StartTime|Speaker|EndTime).*\]', line):
            new_lines.append(line)
            
    return '\n'.join(new_lines) 

def remove_brackets(text):
    return re.sub(r'\[[^\]]*\][ \t]*', '', text)

def remove_asterix(text):
    return re.sub(r'\*[^\s]*', '', text)



if __name__ == '__main__':
    if (len(sys.argv) < 3 or len(sys.argv) > 7):
        print("Usage: python pre_process.py <input_file> <output_file> [remove_time_annotations] [numbers_to_digits] [remove_brackets] [remove_asterix]")   
        sys.exit(1)
    
    remove_time_annotations_option, numbers_to_digits_option, remove_brackets_option, remove_asterix_option = True, True, True, True
    
    input_file, output_file = sys.argv[1], sys.argv[2]
    
    if (len(sys.argv) > 3 and sys.argv[3].lower() == "false"):
        remove_time_annotations_option = False 
    if (len(sys.argv) > 4 and sys.argv[4].lower() == "false"):
        numbers_to_digits_option = False
    if (len(sys.argv) > 5 and sys.argv[5].lower() == "false"):
        remove_brackets_option = False
    if (len(sys.argv) > 6 and sys.argv[6].lower() == "false"):
        remove_asterix_option = False
        
    if (not os.path.exists(input_file)):
        print(f"ERROR: File {input_file} does not exist")
        sys.exit(1)
        
    if (os.path.isdir(input_file)):
        os.makedirs(output_file, exist_ok=True)
        
        for file in os.listdir(input_file):
            input_file_path = os.path.join(input_file, file)
            output_file_path = os.path.join(output_file, file)
            
            with open(input_file_path, 'r') as f:
                text = f.read()
                
                if remove_time_annotations_option:
                    text = remove_time_annotations(text)
                if numbers_to_digits_option:
                    text = numbers_to_digits(text)
                if remove_brackets_option:
                    text = remove_brackets(text)
                if remove_asterix_option:
                    text = remove_asterix(text)
                    
            with open(output_file_path, 'w') as f:
                f.write(text)
                
            print(f"Pre-processed file {input_file_path} and saved to {output_file_path}")
    else: 
        with open(input_file, 'r') as f:
            text = f.read()
            
            if remove_time_annotations_option:
                text = remove_time_annotations(text)
            if numbers_to_digits_option:
                text = numbers_to_digits(text)
            if remove_brackets_option:
                text = remove_brackets(text)
            if remove_asterix_option:
                text = remove_asterix(text)
                
        with open(output_file, 'w') as f:
            f.write(text)
        
        print(f"Pre-processed file {input_file} and saved to {output_file}")
        
    
    