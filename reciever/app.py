import os
import json
from kafka import KafkaConsumer, KafkaProducer
from confluent_kafka import Consumer
from PIL import Image
import base64
import io
import cv2
import numpy as np
import time
from google.protobuf import text_format
from proto_message_pb2 import image
import sys

KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")


consumer = Consumer({'bootstrap.servers': KAFKA_BROKER_URL,
                     'group.id': 'mygroup',
                     'auto.offset.reset': 'earliest'})

consumer.subscribe([TRANSACTIONS_TOPIC])

# consumer = KafkaConsumer(TRANSACTIONS_TOPIC,
#                          bootstrap_servers=KAFKA_BROKER_URL,
#                          value_deserializer=lambda value: json.loads(value),)


def base64_string_to_img(base64_string):
    imgdata = base64.b64decode(base64_string)
    pil_img = Image.open(io.BytesIO(imgdata))
    cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_BGR2RGB)
    return cv2_img


if __name__ == "__main__":
    count_message = 0
    time_thresh = float(1.0)
    count_time = float(0)
    # for msg in consumer:
    #    print(sys.getsizeof(msg))
    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error")
            continue
        count_message += 1
        count_time += float(time.time() - time_start)
        if count_time >= time_thresh:
            print('Message receive per second:', str(count_message/count_time))
            count_message = 0
            count_time = 0
        msg_value = msg.value().decode('utf-8')
        data_string = json.loads(msg_value)
        img_data = data_string['face']
        img = base64_string_to_img(img_data)
    consumer.close()
