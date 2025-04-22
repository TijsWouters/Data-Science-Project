import os
import sys
from tagmapping import *

class Annotation:
    def __init__(self, text, tag, start, end):
        self.text = text
        self.tag = tag
        self.start = start
        self.end = end
        
    def __str__(self):
        return f"<{self.text}>{{{self.tag}}} [{self.start}:{self.end}]"    
    
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
        # Not used in this implementation; annotations are created directly.
        pass

    @staticmethod
    def fromDeduce(annotation):
        mapped_tag = DEDUCE_TAG_MAPPING[annotation.tag]
        return Annotation(annotation.text, mapped_tag, annotation.start_char, annotation.end_char)

    @staticmethod
    def fromDeidentify(annotation):
        mapped_tag = DEIDENTIFY_TAG_MAPPING[annotation.tag]
        return Annotation(annotation.text, mapped_tag, annotation.start, annotation.end)
    
    @staticmethod
    def fromStanza(annotation):
        # Ensure that STANZA_TAG_MAPPING is defined in your tagmapping module.
        mapped_tag = STANZA_TAG_MAPPING[annotation.type]
        return Annotation(annotation.text, mapped_tag, annotation.start_char, annotation.end_char)

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
            if ent.label_ in SPACY_TAG_MAPPING.keys():
                annotation = Annotation.fromSpacy(ent)
                self.addAnnotation(annotation)
    
    def annotateWithNLTK(self):
        annotations = []
        sentences = nltk.sent_tokenize(self.text, language='dutch')
        offset = 0

        for sentence in sentences:
            tokenizer = nltk.tokenize.TreebankWordTokenizer()
            token_spans = list(tokenizer.span_tokenize(sentence))
            tokens = [sentence[start:end] for start, end in token_spans]
            pos_tags = nltk.pos_tag(tokens)

            tree = nltk.ne_chunk(pos_tags)

            token_index = 0 
            for subtree in tree:
                if isinstance(subtree, nltk.Tree):
                    entity_tokens = [leaf[0] for leaf in subtree.leaves()]
                    entity_text = " ".join(entity_tokens)

                    if token_index < len(token_spans):
                        start_char = token_spans[token_index][0]
                    else:
                        start_char = 0

                    end_char = token_spans[token_index][1] if token_index < len(token_spans) else 0
                    for i in range(len(subtree.leaves())):
                        if token_index + i < len(token_spans):
                            end_char = token_spans[token_index + i][1]
                    token_index += len(subtree.leaves())

                    global_start = offset + start_char
                    global_end = offset + end_char
                    nltk_label = subtree.label()

                    mapped_tag = NLTK_TAG_MAPPING[nltk_label]
                    annotation = Annotation(entity_text, mapped_tag, global_start, global_end)
                    annotations.append(annotation)
                else:
                    token_index += 1
            offset += len(sentence) + 1

        self.annotations = annotations
    
    def annotateWithDeduce(self):
        doc = deduce.deidentify(self.text)
        self.annotations = [Annotation.fromDeduce(a) for a in doc.annotations]
    
    def annotateWithDeidentify(self):
        docs = [DeidentifyDocument(name='test', text=self.text)]
        self.annotations = [Annotation.fromDeidentify(a) for a in tagger.annotate(docs)[0].annotations]
    
    def annotateWithStanza(self):
        doc = nlp_stanza(self.text)
        self.annotations = []
        for ent in doc.entities:
            if ent.type in STANZA_TAG_MAPPING.keys():
                annotation = Annotation.fromStanza(ent)
                self.addAnnotation(annotation)
    
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
            # Label entities in the form "<entity_text>{TAG}"
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
    elif method == "stanza":
        document.annotateWithStanza()
        
    if target == "anonymize":
        result = document.anonymize()
    elif target == "label":
        result = document.label()
            
    with open(output_file, 'w') as f:
        f.write(result)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python anonymize.py <method> <target> <input_file> <output_file>")  
        sys.exit(1)
        
    method, target, input_file, output_file = sys.argv[1].lower(), sys.argv[2].lower(), sys.argv[3], sys.argv[4]
    
    if method not in ["spacy", "nltk", "deduce", "deidentify", "stanza"]:
        print(f"ERROR: Method {method} is not supported. Supported methods are 'spacy', 'nltk', 'deduce', 'deidentify', 'stanza'")
        sys.exit(1)
    
    if target not in ["anonymize", "label"]:
        print(f"ERROR: Target {target} is not supported. Supported targets are 'anonymize' and 'label'")
        sys.exit(1)
    
    if not os.path.exists(input_file):
        print(f"ERROR: File {input_file} does not exist")
        sys.exit(1)
        
    if method == "deidentify":
        from deidentify.base import Document as DeidentifyDocument
        from deidentify.tokenizer import TokenizerFactory
        from deidentify.taggers import FlairTagger
        from deidentify.util import mask_annotations
        model = 'model_bilstmcrf_ons_fast-v0.2.0'
        tokenizer = TokenizerFactory().tokenizer(corpus='ons', disable=("tagger", "ner"))
        tagger = FlairTagger(model=model, tokenizer=tokenizer, verbose=False)
    elif method == "spacy":
        import spacy
        nlp = spacy.load("nl_core_news_lg")
    elif method == "nltk":
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('maxent_ne_chunker', quiet=True)
        nltk.download('words', quiet=True)
    elif method == "deduce":
        from deduce import Deduce
        deduce = Deduce()
    elif method == "stanza":
        import stanza
        stanza.download('nl', verbose=False)
        nlp_stanza = stanza.Pipeline('nl', processors='tokenize,ner', use_gpu=False)
       
    if os.path.isdir(input_file):
        os.makedirs(output_file, exist_ok=True)   
        for file in os.listdir(input_file):
            input_file_path = os.path.join(input_file, file)
            output_file_path = os.path.join(output_file, file)
            process_file(input_file_path, output_file_path, method, target)
    else:
        process_file(input_file, output_file, method, target)
