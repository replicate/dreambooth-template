# DreamBooth Template

🦜 Hey! We built an API that automates the whole process outlined below. To get started using that new API, check out the blog post at [replicate.com/blog/dreambooth-api]([https://replicate.com/blog/dreambooth-api])

If you wish to use the old manual method, you can continue reading below.

---

This is a template repo for training and publishing your own custom Stable Diffusion model using Replicate and GitHub Actions.

It uses [replicate.com/replicate/dreambooth](https://replicate.com/replicate/dreambooth) to train the model using your custom imagery.

## Preqrequisites

- A paid Replicate account
- That's it!

## Training the model

1. Fork this repo
1. Copy your Replicate API token from [replicate.com/account](https://replicate.com/account) and use it to [create a repository  secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) named `REPLICATE_API_TOKEN`
1. Add images to the `data` directory of your forked repo.
1. TODO: Set the model name
1. Trigger the workflow

