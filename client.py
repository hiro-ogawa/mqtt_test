import os
from time import sleep
from argparse import ArgumentParser

import paho.mqtt.client as mqtt
from dotenv import load_dotenv
load_dotenv(verbose=True)

topic = os.getenv("TOPIC")
mqtt_endpoint = os.getenv("MQTT_ENDPOINT")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"recv: {msg.topic} {msg.payload.decode('utf-8')}")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("client_mode", choices=["publish", "subscribe"])
    args = parser.parse_args()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_endpoint, 1883, 60)

    if args.client_mode == "publish":
        for i in range(10):
            msg = f"Hello World! {i}"
            client.publish(topic, msg)
            print(f"send: {topic} {msg}")
            sleep(0.5)
    elif args.client_mode == "subscribe":
        client.loop_forever()
    else:
        raise ValueError("Invalid client mode")

