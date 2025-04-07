
# Our tags: NAME, AGE, DATE, LOCATION, ORGANISATION, CONTACT_INFORMATION, IDENTIFIER, OTHER

VALID_TAGS = {
    'NAME',
    'AGE',
    'DATE',
    'LOCATION',
    'ORGANISATION',
    'CONTACT_INFORMATION',
    'IDENTIFIER',
    'OTHER',
}

DEIDENTIFY_TAG_MAPPING = {
    'Address': 'LOCATION',
    'Age': 'AGE',
    'Care_Institute': 'ORGANISATION',
    'Date': 'DATE',
    'Email': 'CONTACT_INFORMATION',
    'Hospital': 'ORGANISATION',
    'ID': 'IDENTIFIER',
    'Initials': 'NAME',
    'Internal_Location': 'LOCATION',
    'Name': 'NAME',
    'Organization_Company': 'ORGANISATION',
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
    'GPE': 'ORGANISATION',
    'NORP': 'ORGANISATION',
    'ORG': 'ORGANISATION',
    'LOC': 'LOCATION',
    'FAC': 'LOCATION',
    'TIME': 'DATE',
    'CARDINAL': 'AGE',
}

DEDUCE_TAG_MAPPING = {
    'patient': 'NAME',
    'persoon': 'NAME',
    'locatie': 'LOCATION',
    'instelling': 'ORGANISATION',
    'datum': 'DATE',
    'leeftijd': 'AGE',
    'patientnummer': 'IDENTIFIER',
    'telefoonnummer': 'CONTACT_INFORMATION',
    'url': 'CONTACT_INFORMATION',
    'ziekenhuis': 'ORGANISATION',
}

NLTK_TAG_MAPPING = {
    "PERSON": "PERSON",
    "ORGANIZATION": "ORGANISATION",
    "GPE": "ORGANISATION",
    "LOCATION": "LOCATION",
    "FACILITY": "LOCATION",
    "DATE": "DATE",
    "GSP": "ORGANISATION",
}