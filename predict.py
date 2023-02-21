import time
import os
from typing import List
import json

from tqdm.auto import tqdm
import torch
from cog import BasePredictor, Input, Path
from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
    PNDMScheduler,
    LMSDiscreteScheduler,
    DDIMScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
)
from diffusers.pipelines.stable_diffusion.safety_checker import (
    StableDiffusionSafetyChecker,
)
from PIL import Image
from transformers import CLIPFeatureExtractor
import shutil
import subprocess

SAFETY_MODEL_CACHE = "diffusers-cache"
SAFETY_MODEL_ID = "CompVis/stable-diffusion-safety-checker"

DEFAULT_HEIGHT = 512
DEFAULT_WIDTH = 512
DEFAULT_SCHEDULER = "DDIM"

# grab instance_prompt from weights,
# unless empty string or not existent

DEFAULT_PROMPT = "a photo of an astronaut riding a horse on mars"


class Predictor(BasePredictor):
    def setup(self):
        self.safety_checker = StableDiffusionSafetyChecker.from_pretrained(
            SAFETY_MODEL_ID,
            cache_dir=SAFETY_MODEL_CACHE,
            torch_dtype=torch.float16,
            local_files_only=True,
        ).to("cuda")
        self.feature_extractor = CLIPFeatureExtractor.from_pretrained(
            "openai/clip-vit-base-patch32", cache_dir=SAFETY_MODEL_CACHE
        )
        self.url = None

    def download_zip_weights_python(self, url):
        """Download the model weights from the given URL"""
        print("Downloading weights...")

        if os.path.exists("weights"):
            shutil.rmtree("weights")
        os.makedirs("weights")

        import zipfile
        from io import BytesIO
        import urllib.request

        url = urllib.request.urlopen(url)
        with zipfile.ZipFile(BytesIO(url.read())) as zf:
            zf.extractall("weights")

    def load_weights(self, url):
        """Load the model into memory to make running multiple predictions efficient"""
        print("Loading Safety pipeline...")

        if url == self.url:
            return

        start_time = time.time()
        self.download_zip_weights_python(url)
        print("Downloaded weights in {:.2f} seconds".format(time.time() - start_time))

        start_time = time.time()
        print("Loading SD pipeline...")
        self.txt2img_pipe = StableDiffusionPipeline.from_pretrained(
            "weights",
            safety_checker=self.safety_checker,
            feature_extractor=self.feature_extractor,
            torch_dtype=torch.float16,
        ).to("cuda")

        self.img2img_pipe = StableDiffusionImg2ImgPipeline(
            vae=self.txt2img_pipe.vae,
            text_encoder=self.txt2img_pipe.text_encoder,
            tokenizer=self.txt2img_pipe.tokenizer,
            unet=self.txt2img_pipe.unet,
            scheduler=self.txt2img_pipe.scheduler,
            safety_checker=self.txt2img_pipe.safety_checker,
            feature_extractor=self.txt2img_pipe.feature_extractor,
        ).to("cuda")
        print("Loaded pipelines in {:.2f} seconds".format(time.time() - start_time))
        self.url = url

    def generate_images(self, images, output_dir):
        with torch.autocast("cuda"), torch.inference_mode():
            pipeline = self.txt2img_pipe
            pipeline.set_progress_bar_config(disable=True)
            for info in tqdm(images, desc="Generating samples"):
                inputs = info.get("input") or info.get("inputs")
                name = info["name"]
                prompt = inputs["prompt"]
                negative_prompt = inputs.get("negative_prompt")
                width = int(inputs.get("width", 512))
                height = int(inputs.get("height", 512))
                num_outputs = int(inputs.get("num_outputs", 1))
                disable_safety_check = bool(inputs.get("disable_safety_check", False))
                num_inference_steps = int(inputs.get("num_inference_steps", 50))
                guidance_scale = float(inputs.get("guidance_scale", 7.5))
                scheduler = inputs.get("scheduler", "DDIM")
                seed = inputs.get("seed")
                if seed is None:
                    seed = int.from_bytes(os.urandom(2), "big")
                else:
                    seed = int(seed)

                pipeline.scheduler = make_scheduler(
                    scheduler, pipeline.scheduler.config
                )
                if disable_safety_check:
                    pipeline.safety_checker = None
                else:
                    pipeline.safety_checker = self.safety_checker

                generator = torch.Generator("cuda").manual_seed(seed)
                output = pipeline(
                    prompt=[prompt] * num_outputs if prompt is not None else None,
                    negative_prompt=[negative_prompt] * num_outputs
                    if negative_prompt is not None
                    else None,
                    guidance_scale=guidance_scale,
                    generator=generator,
                    num_inference_steps=num_inference_steps,
                    width=width,
                    height=height,
                )

                for i, image in enumerate(output.images):
                    if output.nsfw_content_detected and output.nsfw_content_detected[i]:
                        print("skipping nsfw detected for", inputs)
                        continue
                    image.save(os.path.join(output_dir, f"{name}-{i}.png"))

    @torch.inference_mode()
    def predict(
        self,
        images: str = Input(
            description="JSON input",
        ),
        weights: str = Input(
            description="URL to weights",
        ),
    ) -> List[Path]:
        """Run a single prediction on the model"""

        weights = weights.replace(
            "https://replicate.delivery/pbxt/",
            "https://storage.googleapis.com/replicate-files/",
        )

        images_json = json.loads(images)

        if weights is None:
            raise ValueError("No weights provided")
        self.load_weights(weights)

        cog_generated_images = "cog_generated_images"
        if os.path.exists(cog_generated_images):
            shutil.rmtree(cog_generated_images)
        os.makedirs(cog_generated_images)

        self.generate_images(images_json, cog_generated_images)

        directory = Path(cog_generated_images)

        results = []
        for file_path in directory.rglob("*"):
            print(file_path)
            results.append(file_path)
        return results


def make_scheduler(name, config):
    return {
        "PNDM": PNDMScheduler.from_config(config),
        "KLMS": LMSDiscreteScheduler.from_config(config),
        "DDIM": DDIMScheduler.from_config(config),
        "K_EULER": EulerDiscreteScheduler.from_config(config),
        "K_EULER_ANCESTRAL": EulerAncestralDiscreteScheduler.from_config(config),
        "DPMSolverMultistep": DPMSolverMultistepScheduler.from_config(config),
    }[name]
