# Data Science Project: Anonymizing patient-doctor conversations

### Authors
- Bente Bruurs
- Jordi Jesse Verhoeven
- [Tijs Wouters](https://github.com/TijsWouters)

## Project structure
`/audio_snippets`: contains audio snippets that are put in place of parts of the conversation that need to be removed for anonymization, these snippets correspond to the categories of the anonymization process.

`/data`: contains the data used for the project.
- `data/anonymized`: contains anonymized versions of the transcript for each of the methods we used.
- `data/audio`: contains the audio files of the conversations.
- `data/labeled`: contains the labeled version of the transcripts for each method. The manual labeled versions are in the `data/labeled/truth` directory. Difference with the anonymized transcripts is that the labeled transcripts still contain the words that have been marked for removal.
- `data/original`: contains the original transcripts as we received them.
- `data/pre_processed`: contains the pre-processed versions of the original transcripts.

`scripts`: contains the scripts used for the project.
- `scripts/pre_processing`: contains the script used for pre-processing the transcripts and a helper scripts for converting numbers to digits.
- `scripts/anonymize_audio.py`: usage: `python anonymize_audio.py <audio_file> <labeled_file> [<output_file>]`.
- `scripts/anonymize.py`: usage: `python anonymize.py <method> <anonymize|label> <input_file> <output_file>`. Also accepts directories as input.
- `scripts/compare.py`: usage: `python compare.py <labeled_folder>`. Requires there to be a `truth` folder in the labeled folder. 
- `scripts/extract_labels.py`: usage `python extract_labels.py <file_path>`.
- `scripts/labelmapping.py`: helper script for mapping labels from each of the methods to our set of labels.

## Labeling
To label a word or group of words in a conversation we use the following syntax: `<part_to_be_labeled>{label}`.\

We used the following methods to label the data:
- [SpaCy](https://spacy.io/): Popular library for natural language processing in Python.
- [Stanza](https://stanfordnlp.github.io/stanza/): Natural language processing tool made by the Stanford university. 
- [Deduce](https://github.com/vmenger/deduce): rule based model to anonymze medical data.
- [Deidentify](https://github.com/nedap/deidentify): Spacy model that is trained on medical data.

We also manually labeled the data for evaluation purposes. The labeled data can be found in `data/labeled/truth`.

## Evaluation
To evaluate the performance of each method we compare the labels given by a method to the labels given by a human. We use the following metrics:
- TP (True Positive)
- FP (False Positive)
- FN (False Negative)
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1 = 2 * (Precision * Recall) / (Precision + Recall)

## Results
Our results can be found in `RESULTS.md`. Because Deidentify scores the best we also included all mistakes that this method still made in `DEIDENTIFY_MISTAKES.md`.

We report the results for different ways of deciding whether a label is correct:
- **Strict match**: Label, start and end match
- **Position match**: Start and end match, label can be different
- **Larger than match**: Label can be different and label by human is contained within the label by the method, this means the method could have labeled a larger part than the human, but not a smaller part. Example: if the method labels `<18 years old>{age}` and the human labels `<18>{age}`, this is considered correct.

## Anonymizing audio files
To anonymize audio file the original audio file and a labeled transcript are needed as input. We use a `torchaudio.pipelines.MMS_FA` model to align the words of the transcript with the audio. Words that have been labeled are then replaced with a audio snippet of the label. An example of this can be found in `audio_anonymized.wav`.


