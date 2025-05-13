import torch, torchaudio, re
from extract_labels import parse_tags

import re
from num2words import num2words

from pydub import AudioSegment
from pathlib import Path

import sys

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python anonymize_audio.py <audio_file> <labeled_file> <output_file>")
        sys.exit(1)
    
    AUDIO_IN = sys.argv[1]
    LABELED_FILE = sys.argv[2]
    AUDIO_OUT = sys.argv[3] if len(sys.argv) == 4 else "audio_beeped.wav"                  

with open(LABELED_FILE, encoding="utf-8") as f:
    tags, transcript = parse_tags(f.read())
    WORDS = transcript.split()  
    WORDS = [w.replace(".", "") for w in WORDS] 
    WORDS = [num2words(w, lang="nl") if w.isdigit() else w for w in WORDS]  

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

bundle     = torchaudio.pipelines.MMS_FA   
model      = bundle.get_model().to(DEVICE)
tokenizer  = bundle.get_tokenizer()
aligner    = bundle.get_aligner()

wave, sr   = torchaudio.load(AUDIO_IN)
assert sr == bundle.sample_rate            

clips = {}
for f in Path("../audio_snippets").glob("*.mp3"):
    clips[f.stem] = (
        AudioSegment.from_file(f)
        .set_frame_rate(sr)      
        .set_channels(1)
    )

print(clips.keys())

norm = lambda w: re.sub("[^a-z']", "", w.lower())
transcript = [norm(w) for w in WORDS]

with torch.inference_mode():
    emission, _ = model(wave.to(DEVICE))   
    spans       = aligner(emission[0],
                          tokenizer(transcript))

audio_len_sec  = wave.shape[1] / sr         
seconds_per_fr = audio_len_sec / emission.shape[1]

word_times = []
for raw_word, span in zip(WORDS, spans):
    if not span:                            
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
print("Anonymized audio file can be found in: ", AUDIO_OUT)	
    

