import json
import mimetypes
import os
import zipfile

import replicate

MODEL_NAME = "replicate/cog-dreambooth-trainer"
MODEL_VERSION = "b9a7267b10bb9e5fb19eca853ee9582e8838c8cfe1bf174f4cd50991c857992e"

def train():
  print("Training model...")

  print("Checking training data")
  image_count = 0
  for file in os.listdir("data"):
    if mimetypes.guess_type(file)[0].startswith("image/"):
      image_count += 1  
  if image_count == 0:
    raise Exception("No images found in data directory")

  print("Zipping training data")
  with zipfile.ZipFile("data.zip", "w") as zip:
    for file in os.listdir("data"):
      zip.write(os.path.join("data", file))

  print(f"Training on Replicate using model {MODEL_NAME}@{MODEL_VERSION}")
  print(f"https://replicate.com/{MODEL_NAME}/versions/{MODEL_VERSION}")
  model = replicate.models.get(MODEL_NAME)
  version = model.versions.get(MODEL_VERSION)

  output = version.predict(
    instance_prompt= "a photo of sks wearing a top hat",
    class_prompt= "a photo of a person wearing a top hat",
    instance_data=open("data.zip", "rb"))

  print("Done training. Output:\n", json.dumps(output))

  # TODO: download generated weights

if __name__ == "__main__":
    train()