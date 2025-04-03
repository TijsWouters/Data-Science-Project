import os
import sys
from tagmapping import *

class Annotation:
    def __init__(self, text, tag, start, end):
        self.text = text
        self.tag = tag
        self.start = start
        self.end = end
        
    def __eq__(self, value):
        return isinstance(value, Annotation) and self.text == value.text and self.tag == value.tag and self.start == value.start and self.end == value.end

    def __gt__(self, value):
        return isinstance(value, Annotation) and self.start <= value.start and self.end >= value.end
    
    def __lt__(self, value):
        return isinstance(value, Annotation) and self.start >= value.start and self.end <= value.end

    @staticmethod
    def fromSpacy(annotation):
        mapped_tag = SPACY_TAG_MAPPING[annotation.label_]
        return Annotation(annotation.text, mapped_tag, annotation.start_char, annotation.end_char)

    @staticmethod
    def fromNLTK(annotation):
        pass

    @staticmethod
    def fromDeduce(annotation):
        mapped_tag = DEDUCE_TAG_MAPPING[annotation.tag]
        return Annotation(annotation.text, mapped_tag, annotation.start_char, annotation.end_char)

    @staticmethod
    def fromDeidentify(annotation):
        mapped_tag = DEIDENTIFY_TAG_MAPPING[annotation.tag]
        return Annotation(annotation.text, mapped_tag, annotation.start, annotation.end)
    
    
class Document:
    def __init__(self, text):
        self.text = text
        self.annotations = []
        
    def addAnnotation(self, annotation):
        self.annotations.append(annotation)
    
    def addAnnotations(self, annotations):
        self.annotations.extend(annotations)
        
    def annotateWithSpacy(self):
        doc = nlp(self.text)
        self.annotations = []
        for ent in doc.ents:
            if (ent.label_ in SPACY_TAG_MAPPING.keys()):
                annotation = Annotation.fromSpacy(ent)
                self.addAnnotation(annotation)
    
    def annotateWithNLTK(self):
        pass
    
    def annotateWithDeduce(self):
        doc = deduce.deidentify(self.text)
        self.annotations = [Annotation.fromDeduce(a) for a in doc.annotations]
    
    def annotateWithDeidentify(self):
        docs = [DeidentifyDocument(name='test', text=self.text)]
        self.annotations = [Annotation.fromDeidentify(a) for a in tagger.annotate(docs)[0].annotations]
        
    def anonymize(self):
        anonymized_text = self.text
        for annotation in sorted(self.annotations, key=lambda a: a.start, reverse=True):
            label = f"({annotation.tag})"
            text_list = list(anonymized_text)
            text_list[annotation.start:annotation.end] = list(label)
            anonymized_text = "".join(text_list)
        return anonymized_text
    
    def label(self):
        labeled_text = self.text
        for annotation in sorted(self.annotations, key=lambda a: a.start, reverse=True):
            # label 'Bert' as '<Bert>{NAME}'
            label = f"<{annotation.text}>{{{annotation.tag}}}"
            text_list = list(labeled_text)
            text_list[annotation.start:annotation.end] = list(label)
            labeled_text = "".join(text_list)
        return labeled_text

def process_file(input_file, output_file, method, target):
    with open(input_file, 'r') as f:
        text = f.read()
        document = Document(text)
    
    if method == "spacy":
        document.annotateWithSpacy()
    elif method == "nltk":
        document.annotateWithNLTK()
    elif method == "deduce":
        document.annotateWithDeduce()
    elif method == "deidentify":
        document.annotateWithDeidentify()
        
    if target == "anonymize":
        result = document.anonymize()
    elif target == "label":
        result = document.label()
            
    with open(output_file, 'w') as f:
        f.write(result)

if __name__ == "__main__":
    if (len(sys.argv) < 5):
        print("Usage: python anonymize.py <method> <target> <input_file> <output_file>")  
        sys.exit(1)
        
    method, target, input_file, output_file = sys.argv[1].lower(), sys.argv[2].lower(), sys.argv[3], sys.argv[4]
    
    if (method not in ["spacy", "nltk", "deduce", "deidentify"]):
        print(f"ERROR: Method {method} is not supported. Supported methods are 'spacy', 'nltk', 'deduce', and 'deidentify'")
        sys.exit(1)
    
    if (target not in ["anonymize", "label"]):
        print(f"ERROR: Target {target} is not supported. Supported targets are 'anonymize' and 'label'")
    
    if (not os.path.exists(input_file)):
        print(f"ERROR: File {input_file} does not exist")
        sys.exit(1)
        
    if (method == "deidentify"):
        from deidentify.base import Document as DeidentifyDocument
        from deidentify.tokenizer import TokenizerFactory
        from deidentify.taggers import FlairTagger
        from deidentify.util import mask_annotations
        model = 'model_bilstmcrf_ons_fast-v0.2.0'
        tokenizer = TokenizerFactory().tokenizer(corpus='ons', disable=("tagger", "ner"))
        tagger = FlairTagger(model=model, tokenizer=tokenizer, verbose=False)
    elif (method == "spacy"):
        import spacy
        nlp = spacy.load("nl_core_news_lg")
    elif (method == "nltk"):
        pass
    elif (method == "deduce"):
        from deduce import Deduce
        deduce = Deduce()
        
        
    if (os.path.isdir(input_file)):
        os.makedirs(output_file, exist_ok=True)   
        for file in os.listdir(input_file):
            input_file_path = os.path.join(input_file, file)
            output_file_path = os.path.join(output_file, file)
            process_file(input_file_path, output_file_path, method, target)
    else:
        process_file(input_file, output_file, method, target)
        
    