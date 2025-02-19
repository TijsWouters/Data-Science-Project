# Usage: python remove-time-annotations.py <input_file> <output_file>
# Input can be folder, then output will also be a folder

import sys
import os
import re

def remove_time_annotations(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
            
    with open(output_file, 'w') as f:
        for line in lines:
            if not re.match('.*\[(StartTime|Speaker|EndTime).*\]', line):
                f.write(line)
                
def remove_time_annotations_folder(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for file in os.listdir(input_folder):
        input_file = os.path.join(input_folder, file)
        output_file = os.path.join(output_folder, file)
        remove_time_annotations(input_file, output_file)

# Only execute this if this scripts is the main script (e.g. not imported)
if  __name__ == "__main__":
    input_file, output_file = sys.argv[1], sys.argv[2]
    
    if (os.path.isdir(input_file)):
        remove_time_annotations_folder(input_file, output_file)
    else: 
        remove_time_annotations(input_file, output_file)
    print(f"Time annotations removed from {input_file} and saved to {output_file}")
        
        