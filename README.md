# Stable Diffusion Dreambooth model template

This is the template used by [replicate.com dreambooth api](https://replicate.com/blog/dreambooth-api/) to build custom dreambooth models.

This template is based on [cog-stable-diffusion](https://github.com/replicate/cog-stable-diffusion) which uses diffusers.

## Usage

This template is primarily intended for use by [Replicate's DreamBooth API](https://replicate.com/blog/dreambooth-api), which is what you probably want to use to train and publish your own model.

If you really want to use this template locally, you can do so by following these steps:

1. Generate some weights, put them in `weights/` (use our trainer or your own)
2. Download NSFW safety_checker weights using `script/download-weights`
3. Install [cog](https://github.com/replicate/cog) & docker
4. Build `cog build`
5. Predict `cog predict -i prompt="photo of zzz" -i seed=42` ...
