# Image_Kafka

Encode image with full Hd resolution by following these steps: 
	
	1.	Covert into base64 image
	2.	Decode into string type
	3.	json.dumps

Send message via Confluent Kafka. Consumer will do decoding process by reversing the encoding process.

### Docker file

cd into folder:

	1.	docker-compose -f docker.compose.kafka.yml up --build
	2. open a new terminal and typing: docker-compose up --build

That's it. Have fun.
