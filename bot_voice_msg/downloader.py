import os
import sys

import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2ProcessorWithLM

MODEL_ID = "bond005/wav2vec2-large-ru-golos-with-lm"

processor = Wav2Vec2ProcessorWithLM.from_pretrained(MODEL_ID)
model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)
model.save_pretrained("/root/.cache/torch/transformers/bond005/wav2vec2-large-ru-golos-with-lm")

model_conf = {
    "package": sys.argv[1]
}

model_url = model_conf.get("package")
model_dir = "downloaded_model"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, os.path.basename(model_url))

if not os.path.isfile(model_path):
    torch.hub.download_url_to_file(model_url, model_path, progress=True)