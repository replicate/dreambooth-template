<img src="https://i.imgflip.com/70fpy9.jpg">

---

**✋ Notice: This is an experimental project in early development. ✋**

---

This is a template repo for building and publishing your own custom Stable Diffusion model using Replicate.

It uses DreamBooth to train the model using your custom imagery.

## Preqrequisites

- A paid Replicate account
- Access to the Replicate model publishing beta (https://replicate.com/join)
- Cog and Docker installed locally
- You _don't_ need a local GPU

## Usage (Manually training and publishing)

1. Clone this repo.
1. Run `pip install -r requirements.txt`
1. Grab your Replicate API key from https://replicate.com/account and set it as an environment variable: `export REPLICATE_API_TOKEN=<your-token>`.
1. Run `python train.py`. This takes training images, runs them through the [replicate/dreambooth](https://replicate.com/replicate/dreambooth) model, and downloads the resulting model weights. You can provide images in one of three ways:

   - pass a list of training images with `--images image1.jpg another_image.jpg ...`
   - pass a zip of images with `--instance-data my-images.zip`
   - add your images to the data/ folder

   3-5 images is enough but you can add more. You also need to specify two extra parameters:

   - `--instance-prompt`, the prompt identifying your training images
   - `--class-prompt`, the prompt describing images in the same class as your training images

   Note that with the default parameters this will take about **12 minutes** to run.
1. While that's running, go create a new model at https://replicate.com/create (You'll need beta access to do this. If you don't have access, email us at team@replicate.com)
1. Once the `train` script has finished, publish it to the model you created by running

       python publish.py <your-username/your-model>

   By default this will use the weights downloaded by the `train` script. If you want to use some other weights, you can pass them in with `--weights path/to/your/weights`.

## Usage (GitHub Actions)

WIP. See [.github/workflows/train.yaml]([.github/workflows/train.yaml])
