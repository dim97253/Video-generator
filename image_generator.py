from asyncio.windows_events import NULL
import requests
from diffusers import StableDiffusionPipeline
import torch
import base64
import gc


def get_image(prompt):
    # Define the URL and headers
    url = "https://prod-115.westeurope.logic.azure.com:443/workflows/63653803cecf4d9abbefd4381417f41b/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=Y9c6e9_bYMfEmxj00qwNNQxfoBZyK8PgwKju5SA40ro"
    headers = {
        "Content-Type": "application/json"
    }

    # Define your data according to the schema
    data = {
        "model": "diffusion15",
        "neg_prompt": "blur, noise, text, ugly",
        "prompt": prompt,
        "srcimage": "undefined",
        "steps": 30
    }

    # Send the POST request
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        # Assuming the response is just the base64 encoded string without any metadata
        image_base64 = response.text

        # Decode the base64 string to get the binary image data
        image_data = base64.b64decode(image_base64)
        
        return image_data

        # Save the image to a file
        #with open("output_image.png", "wb") as f:
        #    f.write(image_data)
    else:
        print(f"Failed to get image. HTTP Status code: {response.status_code}")
        return NULL

def flush():
  gc.collect()
  torch.cuda.empty_cache()

def get_image_local(prompt):    
    filename = "temp.png"
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    prompt = prompt
    negative_prompt = "blur, noise"
    steps = 120
    image = pipe(prompt = prompt, negative_prompt = negative_prompt, num_inference_steps=steps, width=1136, height=640).images[0]
    
    image.save(filename)
    flush()
    return filename


