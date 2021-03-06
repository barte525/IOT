#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from tkinter import Tk
from pynput.keyboard import Key, Controller

keyboard = Controller()

# The broker name or IP address - seller's PC.
broker = "server"
#broker = "192.168.56.1"

# The MQTT client.
client = mqtt.Client()
client.tls_set("/home/szymcio/IOT/main/main/certs/server_client/ca.crt",
    "/home/szymcio/IOT/main/main/certs/server_client/client.crt",
    "/home/szymcio/IOT/main/main/certs/server_client/client.key",
    tls_version=2)

# Processing message from seller terminal depending on the topic (connections vs scanned cards)
def process_message(client, userdata, message):
    # Decode message.
    message_decoded = str(message.payload.decode("utf-8"))

    # Info about connected devices.
    if message.topic == "seller/connections":
        message_decoded = message_decoded.split(".")
        print(message_decoded[0] + " : " + message_decoded[1])

    # Printing which card was scanned and typing it in the focused place
    else:
        print("Scanned card: " + message_decoded)
        keyboard.type(message_decoded)

# Connect to the broker.
def connect_to_broker():
    client.connect(broker, port=8883)
    client.on_message = process_message
    client.on_disconnect = disconnect_from_broker
    # Starts client and subscribe.
    # Seller's PC is connected only to one terminal, so there's no need to know its id
    # and we can right away subscribe to topic intended for getting messages from terminal
    client.subscribe("seller/connections")
    client.subscribe("seller/terminal")
    client.loop_forever()

# Disconnet the client.
def disconnect_from_broker():
    client.loop_stop()
    client.disconnect()

def run_receiver():
    connect_to_broker()
    #disconnect_from_broker()

if __name__ == "__main__":

    run_receiver()