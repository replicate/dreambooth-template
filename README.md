# DreamBooth Template

🎩🐇 This is a template repo for **training and publishing your own custom DreamBooth model** using Replicate and GitHub Actions.

See our [DreamBooth API blog post](https://replicate.com/blog/dreambooth-api) to learn more.

## Preqrequisites

- A paid [Replicate](https://replicate.com/account) account
- A handful of training images

## Training the model

1. 🍴 Fork and clone this repo.
1. 🐕 Replace the cute puppy images in the `data` directory with your own images in JPEG or PNG format. These can be images of yourself, your pet, your favorite stuffed animal, or any unique object. For best results, these images should contain only the subject itself, with a minimum of background noise or other objects. Use a minimum of three images, but the model will tend to produce better results if you train it with more images, around 10-20.
1. 💾 Commit your changes to git and push to your main branch on GitHub.
1. 🕵️‍♀️ Copy your Replicate API token from [replicate.com/account](https://replicate.com/account) and [create a repository secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) named `REPLICATE_API_TOKEN` with your copied token as the value.
1. 🎬 Trigger the workflow from your GitHub repo page: "Actions" > "Train and publish model" > "Run workflow".
1. ☕️ Depending on the number of training steps you specified when running the workflow, the training process will take 10-30 minutes to run. Go grab a coffee or a snack!

## Running the model

When the training process has completed successfully, it pushes the model to Replicate. You can run it like any other Replicate model, using the website or the API.

To run on the website, go to [your dashboard](https://replicate.com) then click on "Models".

Your new model will be private by default, and only visible to you. If you want anyone to be able to see and run your model, you can make it public in the Settings tab on your model page.

To run the model on the web, enter a prompt using the identifier you specified during training, e.g. `a pencil sketch of zxz`.

To run the model from your own code, click the API tab on your model page for instructions on running with Python, cURL, etc.

To learn more about running models on Replicate, take a look at the [Python getting started guide](https://replicate.com/docs/get-started/python) or the [HTTP API reference](https://replicate.com/docs/reference/http).

If you have questions, open an issue on this repo or find us in [Discord](https://discord.gg/replicate).