import json
import torch
import numpy as npy
from flask import Flask, jsonify, request

app = Flask(__name__)


from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1").to("cuda")


@app.route("/diffusion", methods=["POST"])
def diffusion():
    prompt = request.values.get("prompt")
    color = request.values.get("color")
    style = request.values.get("style")
    pipe_output = pipe(
        prompt=f"{color} {style} of {prompt}",
        negative_prompt="Oversaturated, blurry, low quality",
        height=720,
        width=1280,
        guidance_scale=8,
        num_inference_steps=35,
        generator=torch.Generator(device="cuda").manual_seed(42),
    )
    result = npy.array(pipe_output.images[0])
    image_list = result.tolist()
    return jsonify({"image": image_list})


if __name__ == "__main__":
    with open("./config.json", "r") as config:
        conf = json.load(config)
    host = conf["ListenIP"]
    port = conf["DiffusionPort"]
    app.run(host=host, port=port)
