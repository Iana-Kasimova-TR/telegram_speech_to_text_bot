import os
import ssl

import torch
import yaml
from torch import package

ssl._create_default_https_context = ssl._create_unverified_context

# upload model config
torch.hub.download_url_to_file(
    "https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml",
    "latest_silero_models.yml",
    progress=False,
)
with open("latest_silero_models.yml", "r") as yaml_file:
    models = yaml.load(yaml_file, Loader=yaml.SafeLoader)
model_conf = models.get("te_models").get("latest")

# upload model using PackageImporter
model_url = model_conf.get("package")
model_dir = "downloaded_model"
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, os.path.basename(model_url))
if not os.path.isfile(model_path):
    torch.hub.download_url_to_file(model_url, model_path, progress=True)
imp = package.PackageImporter(model_path)
model = imp.load_pickle("te_model", "model")


def enhance_text(text: str) -> str:
    return model.enhance_text(text, lan="ru")
