# image-prediction
simple api for image detection and classification using yolo and imagenet

build docker image with:
```
docker build -t image-prediction .
```

run docker image using:
```
docker run --network=host image-prediction
```

API usage:
* /info - basic project info
* /detection - image detection using yolo
* /classification - image classification with imagenet1k

local usage eхample 
```
curl -X POST -F image=@{IMAGE PATH} 'http://localhost:5000/classification'
```

Ссылка на dockerhub https://hub.docker.com/r/tanyaoley/image-prediction

```
docker pull tanyaoley/image-prediction
```
