# cog-dreambooth

Provide your customized images, train your own dreambooth model, and share on Replicate!


## Preqrequisites

- A paid Replicate account
- Access to the Replicate model publishing beta (https://replicate.com/join)
- Cog and Docker installed locally

## Usage (Manually training and publishing)

1. Add 3-5 jpeg images to the `data` folder.
1. Run `pip install -r requirements.txt`
1. Run `python train.py`. This will take about 20 minutes.
1. While that's running, go create a model at https://replicate.com/create
1. Edit `cog.yaml` and set `image: r8.im/your-username/your-model-name`
1. `cog login`
1. Edit `predict.py` and set `DREAMBOOTH_MODEL_PATH` to the path to the downloaded weights. Something like `weights/data/100`, where `100` is the checkpoint you want to use.
1 `cog push`

## Usage (GitHub Actions)

WIP...

1. Add 3-5 jpeg images to the `data` folder.
1. Run `pip install -r requirements.txt`
1. Get your Replicate API token from [replicate.com/account](https://replicate.com/account) and set it as an environment variable: `export REPLICATE_API_TOKEN=...`
1. Run `python train.py`