import json
import os
import numpy as np
import torch
from flask import Flask, request
from PIL import Image
import io
from torchvision import transforms
import pickle

app = Flask(__name__)

@app.route('/info')
# Returns project info
def get_project_info():
    return {'prolect_info': 'project for image detection and classification'}


@app.route('/detection', methods=['POST'])
def detection():

    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    model.eval()
    if not request.method == 'POST':
        return

    
    if request.files.get('image'):
      
        image_file = request.files['image']
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))
    
        results = model(img, size=640)
        return results.pandas().xyxy[0].to_json(orient='records')


@app.route('/classification', methods=['POST'])
def classification():
    model = torch.hub.load('facebookresearch/semi-supervised-ImageNet1K-models', 'resnet18_swsl')
    model.eval()
    if not request.method == 'POST':
        return
    
    if request.files.get('image'):
      
        image_file = request.files['image']
        image_bytes = image_file.read()

        img = Image.open(io.BytesIO(image_bytes))
        preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        input_tensor = preprocess(img)
        input_batch = input_tensor.unsqueeze(0) 
       
        if torch.cuda.is_available():
            input_batch = input_batch.to('cuda')
            model.to('cuda')

        with torch.no_grad():
            output = model(input_batch)
        result = np.argmax(torch.nn.functional.softmax(output[0], dim=0).numpy())
    
        return str(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')