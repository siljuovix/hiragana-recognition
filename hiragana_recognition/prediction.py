import numpy as np
from PIL import Image
import PIL.ImageOps
from hiragana_recognition import model

import torch
from torchvision import transforms


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
net = model.Net()
net = net.to(device)
net.load_state_dict(torch.load("hiragana_recognition/models/hiragana_10_epoch_no_aug.pth"))


def inference(input_image):
    with torch.no_grad():
      net.eval()
      input_image = input_image.unsqueeze(0)
      input_image = input_image.to(device)
      output =net(input_image)
      index = output.data.cpu().numpy().argmax()
      return index
