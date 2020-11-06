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


if __name__ == "__main__":
    count_message = 0
    time_thresh = float(1.0)
    count_time = float(0)
    # for msg in consumer:
    #    print(sys.getsizeof(msg))
    while True:
        time_start = float(time.time())
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
        # print(msg.value())
        # print('receive')
        # msg_value = msg.value().decode('utf-8')
#        # print(msg_value)
        # msg = text_format.Merge(text=msg_value, message=image)
#        b_decode = (msg.img_b).decode('utf-8')
#        # print(type(b_decode))
#        b_np = np.frombuffer((msg.img_b), np.uint8)
#        g_np = np.frombuffer((msg.img_g), np.uint8)
#        r_np = np.frombuffer((msg.img_r), np.uint8)
#        print(r_np.shape)
#        # f = open("arr.txt", "w")
#        # f.write(r_np)
#        # f.close()
#        # f_ = open('str.txt', 'w')
#        # f_.write((msg.img_g).decode('utf-8'))
#        # f_.close()
#        # print('File wrote')
#        img_bgr = cv2.merge((b_np, g_np, r_np))
#        height, width, channels = img_bgr.shape
#        # print(img_bgr.shape)
#        # print(len((msg.img_g).decode('utf-8')))
#        # print(g_np.shape)
#        # print(height, width, channels)
#        image_np = np.fromstring((msg.image).decode('utf-8'), np.uint8)
#        # print(image_np.shape)
#        # image_string = (msg.image).decode('utf-8')
#        # print(image_string)
#        # image_numpy = np.fromstring(image_string, np.uint8)
#
#        # print(b_decode)
#        # b_arr = np.fromstring(b_decode)
#        # print(b_arr)
#        # print(type((msg.img_data).decode('utf-8')))
#        # msg_value = eval(msg_value)
#        # print(type(msg_value))
#        # print(type(msg.value))
#        # print(msg)
#        # value_decode_byte = msg.value().decode('utf-8')
#        # value_decode_json = json.loads(value_decode_byte)
#        # value_img = value_decode_json['face']
#        # img = base64_string_to_img(value_img)
#        # print(img[:2])
#        # print('Received message')

    consumer.close()
