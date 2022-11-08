# cog-dreambooth

Provide your customized images, train your own dreambooth model, and share on Replicate!

## Usage

1. Add 3-5 images to the `data` folder. They can be JPGs or PNGs. Size doesn't matter.
1. Run `pip install -r requirements.txt`
1. Get your Replicate API token from [replicate.com/account](https://replicate.com/account) and set it as an environment variable: `export REPLICATE_API_TOKEN=...`
1. Run `python train.py`