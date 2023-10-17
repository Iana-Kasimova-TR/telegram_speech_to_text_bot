import os
import warnings

import librosa
import nltk
import numpy as np
import torch
from datasets import load_dataset
from transformers import Wav2Vec2ForCTC, Wav2Vec2ProcessorWithLM

MODEL_ID = "bond005/wav2vec2-large-ru-golos-with-lm"


# nltk.download("punkt")

num_processes = max(1, os.cpu_count())

#for LOCAL
#processor = Wav2Vec2ProcessorWithLM.from_pretrained(MODEL_ID)
#model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)


# REMOTE
model = Wav2Vec2ForCTC.from_pretrained('/root/.cache/torch/transformers/bond005/wav2vec2-large-ru-golos-with-lm')
processor = Wav2Vec2ProcessorWithLM.from_pretrained('/root/.cache/torch/transformers/bond005/wav2vec2-large-ru-golos-with-lm')


def get_text(path: str):
    print(path)
    audio, __ = librosa.load(path, duration=5.0)
    print(audio)
    input = processor(audio, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(input.input_values, attention_mask=input.attention_mask).logits
    predicted_resp = processor.batch_decode(
        logits.numpy(), num_processes=num_processes
    ).text
    return predicted_resp
