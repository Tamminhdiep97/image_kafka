"""Produce fake transactions into a Kafka topic."""
import os
import time
from time import sleep
import json
import base64
import cv2
import sys
import numpy as np
import zlib

from confluent_kafka import Producer
from kafka import KafkaProducer
from transactions import create_random_transaction
from proto_message_pb2 import image
from google.protobuf import text_format


TRANSACTIONS_TOPIC = os.environ.get('TRANSACTIONS_TOPIC')
KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TRANSACTIONS_PER_SECOND = float(os.environ.get('TRANSACTIONS_PER_SECOND'))
SLEEP_TIME = 1 / TRANSACTIONS_PER_SECOND

producer = Producer({'bootstrap.servers': KAFKA_BROKER_URL,
                     'group.id': 'mygroup',
                     'auto.offset.reset': 'earliest'})


# producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL)

def img_to_base64_string(img) -> dict:
    '''create face to send topic'''
    is_success, im_buf_arr = cv2.imencode(".jpg", img)
    img_base64 = base64.b64encode(im_buf_arr)
    base64_string = img_base64.decode('utf-8')

    return {
        'face': base64_string,
    }

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))


if __name__ == '__main__':
    image_cv = cv2.imread('fullhd.jpg')
    time_thresh = float(1.0)
    count_time = float(0)
    while True:
        key_time = time.time()
        base64_string = img_to_base64_string(image_cv)
        # print(sys.getsizeof(b_np.tobytes()))
        img_json = json.dumps(base64_string)
        # print(sys.getsizeof(bytes(msg_obj)))
        msg_value = text_format.MessageToString(msg_obj, as_utf8=True,
                                                double_format='.17g')
#        print(os.getcwd())
        # img = cv2.imread('fullhd.jpg')
        # data = img_to_base64_string(img)
        # json_data = json.dumps(data)
        # producer.poll(0)
        # producer.send(TRANSACTIONS_TOPIC, value=msg_value)
        producer.produce(TRANSACTIONS_TOPIC,
                         value=img_json,
                         callback=delivery_report)
        # print(type((str(msg_obj)).encode('utf-8')))
        # producer.produce(TRANSACTIONS_TOPIC,
        #                  value=msg_value,
        #                  callback=delivery_report)
        # # transaction = 'Text Message'
        # print(transaction)  # DEBUG
        # sleep(SLEEP_TIME)
        count_msg += 1
        count_time += float(time.time() - key_time)
        if count_time >= time_thresh:
            print('Message send per second:', str(count_msg/count_time))
            count_msg = 0
            count_time = 0
    producer.flush()
