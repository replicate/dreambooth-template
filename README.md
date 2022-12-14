# Stable Diffusion Dreambooth model template

This is the template used by [replicate.com dreambooth api](https://replicate.com/blog/dreambooth-api/) to build custom dreambooth models.

This template is based on [cog-stable-diffusion](https://github.com/replicate/cog-stable-diffusion) which uses diffusers.

## How to use this template

Ignore this template and use our [replicate.com dreambooth api](https://replicate.com/blog/dreambooth-api/).  It will generate an HTTP API for you generate images from your model.

## How to use this template locally

If you really want to use this template locally, you can do so by following these steps:

1. Generate some weights, put them in `weights/` (use our trainer or your own)
2. Install [cog](https://github.com/replicate/cog) & docker
3. Build `cog build`
4. Predict `cog predict -i prompt="photo of zzz" -i seed=42` ...
