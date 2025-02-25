import os
import sys

# Dictionary for base numbers
numwords = {
    "nul": 0,
    "een": 1,
    "twee": 2,
    "drie": 3,
    "vier": 4,
    "vijf": 5,
    "zes": 6,
    "zeven": 7,
    "acht": 8,
    "negen": 9,
    "tien": 10,
    "elf": 11,
    "twaalf": 12,
    "dertien": 13,
    "veertien": 14,
    "vijftien": 15,
    "zestien": 16,
    "zeventien": 17,
    "achttien": 18,
    "negentien": 19,
    "twintig": 20,
    "dertig": 30,
    "veertig": 40,
    "vijftig": 50,
    "zestig": 60,
    "zeventig": 70,
    "tachtig": 80,
    "negentig": 90,
}

def parse_tens(s: str) -> int:
    """
    Parses a number below 100 (possibly including numbers like "eenentwintig").
    """
    if s == "":
        return 0
    if s in numwords:
        return numwords[s]
    # Look for pattern: unit + "en" + tens (e.g., "vijfenvijftig" -> 5 + 50)
    for unit in ["een", "twee", "drie", "vier", "vijf", "zes", "zeven", "acht", "negen"]:
        prefix = unit + "en"
        if s.startswith(prefix):
            tens_part = s[len(prefix):]
            if tens_part in numwords and numwords[tens_part] >= 20:
                return numwords[unit] + numwords[tens_part]
    raise ValueError(f"Unknown tens value: {s}")

def parse_hundred(s: str) -> int:
    """
    Parses a number below 1000.
    Looks for the presence of "honderd" and splits the string accordingly.
    """
    if s == "":
        return 0
    idx = s.find("honderd")
    if idx != -1:
        hundreds_part = s[:idx]
        rest = s[idx+len("honderd"):]
        # If nothing appears before "honderd", it means 1 hundred.
        if hundreds_part == "":
            hundreds = 1
        else:
            hundreds = parse_tens(hundreds_part)
        remainder = parse_tens(rest) if rest else 0
        return hundreds * 100 + remainder
    else:
        return parse_tens(s)

def parse_number(text: str) -> int:
    """
    Parses a fully spelled out Dutch number (as text) into its integer value.
    Handles numbers under one million.
    """
    # Preprocessing: lowercase and remove spaces and hyphens
    s = text.lower().replace(" ", "").replace("-", "")
    if s == "":
        raise ValueError("Input string is empty")
    if s == "nul":
        return 0
    # Check for "duizend" (thousands)
    idx = s.find("duizend")
    if idx != -1:
        thousands_part = s[:idx]
        rest = s[idx+len("duizend"):]
        # If no number precedes "duizend", it is implicitly 1 thousand.
        if thousands_part == "":
            thousands = 1
        else:
            thousands = parse_hundred(thousands_part)
        remainder = parse_hundred(rest) if rest else 0
        number = thousands * 1000 + remainder
    else:
        number = parse_hundred(s)
    if number >= 1000000:
        raise ValueError("Number is one million or greater; only numbers under one million are supported.")
    return number

def numbers_to_digits(input_file, output_file):
    with open(input_file, 'r', encoding='utf8') as f:
        text = f.read()
        
    # Change numbers to digit for each sentence
    sentences = text.split("\n")
    for i, sentence in enumerate(sentences):
        words = sentence.split(" ")
        for j, word in enumerate(words):
            try:
                number = parse_number(word)
                words[j] = str(number)
            except ValueError:
                pass
        sentences[i] = " ".join(words)
    
    with open(output_file, 'w', encoding='utf8') as f:
        f.write("\n".join(sentences))
        
def folder_numbers_to_digits(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        numbers_to_digits(input_path, output_path)

# Example usage:
if __name__ == "__main__":
    input_file, output_file = sys.argv[1], sys.argv[2]
    if (os.path.isdir(input_file)):
        folder_numbers_to_digits(input_file, output_file)
    else:
        numbers_to_digits(input_file, output_file)
    
    print(f"Numbers changed to digits in {input_file} and saved to {output_file}")
