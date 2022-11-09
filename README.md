# cog-dreambooth

This is a template repo for building and publishing your own custom Stable Diffusion model using Replicate.

It uses DreamBooth to train the model using your custom imagery.

## Preqrequisites

- A paid Replicate account
- Access to the Replicate model publishing beta (https://replicate.com/join)
- Cog and Docker installed locally

## Usage (Manually training and publishing)

1. Fork and clone this repo.
1. Add 3-5 jpeg images to the `data` folder.
1. Run `pip install -r requirements.txt`
1. Grab your Replicate API key from https://replicate.com/settings and set it as an environment variable: `export =REPLICATE_API_TOKEN=<your-token>`.
1. Run `python train.py`. This scripts zips the images in the data folder, runs them through the [replicate/cog-dreambooth-trainer](https://replicate.com/replicate/cog-dreambooth-trainer) model, and downloads the resulting model weights. This will take about **20 minutes**.
1. While that's running, go create a new model at https://replicate.com/create (You'll need beta access to do this. If you don't have access, email us at team@replicate.com)
1. Edit `cog.yaml` and set `image: r8.im/your-username/your-model`
1. `cog login`
1. Edit `predict.py` and set `DREAMBOOTH_MODEL_PATH` to the path of the downloaded weights. Something like `weights/data/100`, where `100` is the checkpoint you want to use
1. `cog push`

## Usage (GitHub Actions)

WIP. See [.github/workflows/train.yaml]([.github/workflows/train.yaml])