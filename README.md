<img src="https://i.imgflip.com/70fpy9.jpg">

---

# DreamBooth Template

**✋ Notice: This is an experimental project in early development. ✋**

This is a template repo for training and publishing your own custom Stable Diffusion model using Replicate.

It uses [replicate.com/replicate/dreambooth](https://replicate.com/replicate/dreambooth) to train the model using your custom imagery.

## Preqrequisites

- A paid Replicate account
- Cog and Docker installed locally
- Access to the Replicate [model publishing beta](https://replicate.com/join)
- You _don't_ need a local GPU

## Training the model

1. Clone this repo.
1. Run `pip install -r requirements.txt`
1. Grab your Replicate API key from https://replicate.com/account and set it as an environment variable: `export REPLICATE_API_TOKEN=<your-token>`.
1. Run `python train.py`. This takes training images, runs them through the [replicate/dreambooth](https://replicate.com/replicate/dreambooth) model, and downloads the resulting model weights. You can provide images in one of three ways:

   - pass a list of training images with `--images image1.jpg another_image.jpg ...`
   - pass a zip of images with `--instance-data my-images.zip`
   - add your images to the data/ folder. (If you use this option, delete the default cute puppy pictures in the folder first! 🐾)

   3-5 images is enough but you can add more. You also need to specify two extra parameters:

   - `--instance-prompt`, the prompt identifying your training images
   - `--class-prompt`, the prompt describing images in the same class as your training images

   Note that with the default parameters this will take about **12 minutes** to run.

## Publishing the model

The training process creates, downloads, and extracts trained weights for your custom model. If you've got a machine with a GPU, you can run your custom model locally using `cog predict`, but you can also publish it to Replicate so that anyone can run it from the web or using Replicate's API:

1. Create a new model at https://replicate.com/create (You'll need beta access to do this. If you don't have access, you can [join the waitlist](https://replicate.com/join).)
1. Once the `train` script has finished, publish it to the model you created by running

       python publish.py <your-username/your-model>

   By default this will use the weights downloaded by the `train` script. If you want to use some other weights, you can pass them in with `--weights path/to/your/weights`.
