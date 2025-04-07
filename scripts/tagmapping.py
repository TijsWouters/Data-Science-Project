
# Our tags: NAME, AGE, DATE, LOCATION, ORGANIZATION, CONTACT_INFORMATION, IDENTIFIER, OTHER

VALID_TAGS = {
    'NAME',
    'AGE',
    'DATE',
    'LOCATION',
    'ORGANIZATION',
    'CONTACT_INFORMATION',
    'IDENTIFIER',
    'OTHER',
}

DEIDENTIFY_TAG_MAPPING = {
    'Address': 'LOCATION',
    'Age': 'AGE',
    'Care_Institute': 'ORGANIZATION',
    'Date': 'DATE',
    'Email': 'CONTACT_INFORMATION',
    'Hospital': 'ORGANIZATION',
    'ID': 'IDENTIFIER',
    'Initials': 'NAME',
    'Internal_Location': 'LOCATION',
    'Name': 'NAME',
    'Organization_Company': 'ORGANIZATION',
    'Other': 'OTHER',
    'Phone_Fax': 'CONTACT_INFORMATION',
    'Profession': 'OTHER',
    'SSN': 'IDENTIFIER',
    'URL_IP': 'CONTACT_INFORMATION',
}

SPACY_TAG_MAPPING = {
    'PERSON': 'NAME',
    'DATE': 'DATE',
    'EVENT': 'DATE',
    'GPE': 'ORGANIZATION',
    'NORP': 'ORGANIZATION',
    'ORG': 'ORGANIZATION',
    'LOC': 'LOCATION',
    'FAC': 'LOCATION',
    'TIME': 'DATE',
    'CARDINAL': 'AGE',
}

DEDUCE_TAG_MAPPING = {
    'patient': 'NAME',
    'persoon': 'NAME',
    'locatie': 'LOCATION',
    'instelling': 'ORGANIZATION',
    'datum': 'DATE',
    'leeftijd': 'AGE',
    'patientnummer': 'IDENTIFIER',
    'telefoonnummer': 'CONTACT_INFORMATION',
    'url': 'CONTACT_INFORMATION',
    'ziekenhuis': 'ORGANIZATION',
}

NLTK_TAG_MAPPING = {
    "PERSON": "PERSON",
    "ORGANIZATION": "ORGANIZATION",
    "GPE": "ORGANIZATION",
    "LOCATION": "LOCATION",
    "FACILITY": "LOCATION",
    "DATE": "DATE",
    "GSP": "ORGANIZATION",
}