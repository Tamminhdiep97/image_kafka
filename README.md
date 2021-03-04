# Image_Kafka

Encode image with full Hd resolution by following these steps:
```console
	
	1.	Covert into base64 image
	2.	Decode into string type
	3.	json.dumps
```
Send message via Confluent Kafka. Consumer will do decoding process by reversing the encoding process.

### Docker file

cd into folder:
```console
docker-compose -f docker.compose.kafka.yml up --build
open a new terminal and typing: docker-compose up --build
```

Inspited by my Mentor: https://github.com/huutrinh68 and https://florimond.dev/blog/articles/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/ 

That's it. Have fun.
