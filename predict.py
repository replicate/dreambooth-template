import os
import shutil
from typing import List
import torch
from diffusers import StableDiffusionPipeline, DDIMScheduler
from pytorch_lightning import seed_everything
from cog import BasePredictor, Input, Path


DREAMBOOTH_MODEL_PATH = "weights"


class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        scheduler = DDIMScheduler(
            beta_start=0.00085,
            beta_end=0.012,
            beta_schedule="scaled_linear",
            clip_sample=False,
            set_alpha_to_one=False,
        )
        self.pipe = StableDiffusionPipeline.from_pretrained(
            DREAMBOOTH_MODEL_PATH,
            scheduler=scheduler,
            safety_checker=None,
            torch_dtype=torch.float16,
        ).to("cuda")

    @torch.inference_mode()
    @torch.cuda.amp.autocast()
    def predict(
        self,
        prompt: str = Input(
            description="Input prompt",
            default="a cjw cat in a bucket",
        ),
        negative_prompt: str = Input(description="The prompt NOT to guide the image generation. Ignored when not using guidance", default=None),
        width: int = Input(
            description="Width of output image. Maximum size is 1024x768 or 768x1024 because of memory limits",
            choices=[128, 256, 512, 768, 1024],
            default=512,
        ),
        height: int = Input(
            description="Height of output image. Maximum size is 1024x768 or 768x1024 because of memory limits",
            choices=[128, 256, 512, 768, 1024],
            default=512,
        ),
        num_outputs: int = Input(
            description="Number of images to output", choices=[1, 4], default=1
        ),
        num_inference_steps: int = Input(
            description="Number of denoising steps", ge=1, le=500, default=50
        ),
        guidance_scale: float = Input(
            description="Scale for classifier-free guidance", ge=1, le=20, default=7.5
        ),
        seed: int = Input(
            description="Random seed. Leave blank to randomize the seed", default=None
        ),
    ) -> List[Path]:
        """Run a single prediction on the model"""

        print("Loading pipeline...")

        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")
        print(f"Using seed: {seed}")

        if width == height == 1024:
            raise ValueError(
                "Maximum size is 1024x768 or 768x1024 pixels, because of memory limits. Please select a lower width or height."
            )

        seed_everything(seed)

        output = self.pipe(
            prompt=[prompt] * num_outputs,
            negative_prompt=[negative_prompt] * num_outputs if negative_prompt is not None else None,
            width=width,
            height=height,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
        )

        output_paths = []
        for i, sample in enumerate(output["images"]):
            output_path = f"/tmp/out-{i}.png"
            sample.save(output_path)
            output_paths.append(Path(output_path))

        return output_paths
