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
      seed=1337,
      adam_beta1=0.9,
      adam_beta2=0.999,
      resolution=512,
      adam_epsilon=1e-08,
      class_prompt="a photo of a person wearing a top hat",
      lr_scheduler='constant',
      instance_data=open("data.zip", "rb"),
      # instance_data='https://replicate.delivery/pbxt/HkTENyq0Ph5hzI3HgumA1HTZzycUNp8qWL2n2SnzuaHZpIP4/Archive.zip',
      learning_rate=1e-06,
      max_grad_norm=1,
      n_save_sample=4,
      save_interval=10000,
      use_8bit_adam=True,
      instance_prompt="a photo of sks wearing a top hat",
      max_train_steps=500,
      num_class_images=50,
      num_train_epochs=1,
      save_infer_steps=50,
      train_batch_size=1,
      adam_weight_decay=0.01,
      prior_loss_weight=1,
      sample_batch_size=4,
      train_text_encoder=True,
      save_guidance_scale=7.5,
      gradient_checkpointing=True,
      with_prior_preservation=True,
      gradient_accumulation_steps=1,
  )

  print("Done training. Output:\n", json.dumps(output))

  # TODO: download generated weights

if __name__ == "__main__":
    train()