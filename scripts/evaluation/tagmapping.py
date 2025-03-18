
# Our tags: NAME, DATE, LOCATION, ORGANIZATION, AGE, CONTACT_INFORMATION, IDENTIFIER, OTHER

DEIDENTIFY_TAG_MAPPING = {
    'Address': 'LOCATION',
    'Age': 'AGE',
    'Care_Institution': 'ORGANIZATION',
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
    'PATIENT': 'NAME',
    'PERSOON': 'NAME',
    'LOCATIE': 'LOCATION',
    'INSTELLING': 'ORGANIZATION',
    'DATUM': 'DATE',
    'LEEFTIJD': 'AGE',
    'PATIENTNUMMER': 'IDENTIFIER',
    'TELEFOONNUMMER': 'CONTACT_INFORMATION',
    'URL': 'CONTACT_INFORMATION',
}