# image-prediction
simple api for image detection and classification using yolo and imagenet

build docker image with:
```
sudo  docker build -t image-prediction .
```

run docker image using:
```
sudo docker run --network=host image-prediction
```

API usage:
* /info - basic project info
* /detection - image detection using yolo
* /classification - image classification with imagenet1k

local usage eхample 
```
curl -X POST -F image=@{IMAGE PATH} 'http://localhost:5000/classification'
```
