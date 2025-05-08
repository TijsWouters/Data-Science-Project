import torch, torchaudio, re, json
from extract_labels import parse_tags

import re, unicodedata
from num2words import num2words

from pydub import AudioSegment, effects
from pathlib import Path



AUDIO  = "../data/audio/he-knmp-2018.wav"                    # 16-kHz mono is ideal

with open("../data/labeled/truth/he-knmp-2018.txt", encoding="utf-8") as f:
    tags, transcript = parse_tags(f.read())
    WORDS = transcript.split()  
    WORDS = [w.replace(".", "") for w in WORDS]  # remove trailing dot
    WORDS = [num2words(w, lang="nl") if w.isdigit() else w for w in WORDS]  # convert digits to words

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

bundle     = torchaudio.pipelines.MMS_FA     # multilingual model incl. Dutch
model      = bundle.get_model().to(DEVICE)
tokenizer  = bundle.get_tokenizer()
aligner    = bundle.get_aligner()

wave, sr   = torchaudio.load(AUDIO)
assert sr == bundle.sample_rate             # MMS models expect 16 kHz

clips = {}
for f in Path("../audio_snippets").glob("*.mp3"):
    clips[f.stem] = (
        AudioSegment.from_file(f)
        .set_frame_rate(sr)       # resample to match main file
        .set_channels(1)
    )

print(clips.keys())

# minimal Dutch normalisation – trailing punctuation, case, diacritics
norm = lambda w: re.sub("[^a-z']", "", w.lower())
transcript = [norm(w) for w in WORDS]

with torch.inference_mode():
    emission, _ = model(wave.to(DEVICE))    # (B, T, vocab)
    spans       = aligner(emission[0],
                          tokenizer(transcript))

audio_len_sec  = wave.shape[1] / sr           # total seconds
seconds_per_fr = audio_len_sec / emission.shape[1]

word_times = []
for raw_word, span in zip(WORDS, spans):
    if not span:                             # ← empty alignment
        start = 0
        end   = 0
        word_times.append({"word": raw_word, "start": start, "end": end})
        print(f"⚠️  no alignment for “{raw_word}”, skipping")
        continue

    start = round(span[0].start * seconds_per_fr, 2)
    end   = round(span[-1].end  * seconds_per_fr, 2)
    word_times.append({"word": raw_word, "start": start, "end": end})
    
from pydub import AudioSegment
from pydub.generators import Sine

AUDIO_IN = "../data/audio/he-knmp-2018.wav"
AUDIO_OUT = "audio_beeped.wav"

# ----------------------------------------------------------------------
# 1) load the audio (pydub works in milliseconds)
orig = AudioSegment.from_file(AUDIO_IN)
sr   = orig.frame_rate               # keep the original sample-rate

# 2) for every index → build & overlay a beep segment
tone  = Sine(1000, sample_rate=sr)   # 1 kHz, matches speech band
for tag in sorted(tags, key=lambda tag: tag[4], reverse=True):
    cat      = tag[1].lower()
    repl_src = clips[cat]
    
    t0_ms = int(word_times[tag[4]]["start"] * 1000)
    
    t1_ms = int(word_times[tag[4] + tag[5] - 1]["end"]   * 1000)

    orig = orig[:t0_ms] + repl_src + orig[t1_ms:]

# 3) export; pydub chooses codec by extension
orig.export(AUDIO_OUT, format="wav")
print("✅  done →", AUDIO_OUT)
    

