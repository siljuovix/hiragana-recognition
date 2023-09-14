from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import torch
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request

import numpy as np
from PIL import Image
import PIL.ImageOps
from hiragana_recognition import model
from hiragana_recognition import prediction
import logging

import torch
from torchvision import transforms
import base64
import io



app = FastAPI()

# WIP: fix path
app.mount("/static", StaticFiles(directory=r"C:\Users\Silvia\hiragana-recognition\app\static"), name="static")

def process_image(image):
    transform = transforms.Compose([transforms.ToTensor(), transforms.Grayscale(num_output_channels=1), transforms.Normalize((0.5, ), (0.5, ))])
    image = image.resize((28, 28), Image.Resampling.LANCZOS)
    image = PIL.ImageOps.invert(image)
    image.save("input_image.jpeg")
    image = transform(image).float()
    return image

class ImageData(BaseModel):
    image_data: str

@app.post("/predict")
async def predict(image_data: ImageData):
    try:
        base64_data = image_data.image_data.split(',')[1]
        decoded_image = base64.b64decode(base64_data)
        image = Image.open(io.BytesIO(decoded_image))
        print("Image Mode:", image.mode)
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, (0, 0), image)
        image_tensor = process_image(background)
        predicted = prediction.inference(image_tensor)

        response = {"prediction": predicted.item()}
        print(response)
        return response
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
