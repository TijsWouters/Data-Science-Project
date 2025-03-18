from tagmapping import *

class Annotation:
    def __init__(self, text, tag, start, end):
        self.text = text
        self.tag = tag
        self.start = start
        self.end = end

    @staticmethod
    def fromSpacy(annotation):
        return Annotation(annotation.text, annotation.label_, annotation.start_char, annotation.end_char)

    @staticmethod
    def fromNLTK(annotation):
        pass

    @staticmethod
    def fromDeduce(annotation):
        return Annotation(annotation.text, annotation.tag, annotation.start_char, annotation.end_char)

    @staticmethod
    def fromDeidentify(annotation):
        mapped_tag = DEIDENTIFY_TAG_MAPPING[annotation.tag]
        return Annotation(annotation.text, mapped_tag, annotation.start, annotation.end)
