#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from tkinter import Tk
# When used on windows requires pywin32 library installed (not imported, f.e. via pip)
# or Xclip package on Linux (f.e. via apt-get)
import xerox

# The broker name or IP address - seller's PC.
broker = "localhost"
#broker = "192.168.56.1"

# The MQTT client.
client = mqtt.Client()

# # Processing message from seller terminal depending on the topic (connections vs scanned cards)
def process_message(client, userdata, message):
    # Decode message.
    message_decoded = str(message.payload.decode("utf-8"))

    # Info about connected devices and subscribing to topic related to given terminal.
    if message.topic == "seller/connections":
        message_decoded = message_decoded.split(".")
        print(message_decoded[0] + " : " + message_decoded[1])
    # Printing which card was scanned and copying its id to the clipboard
    else:
        print("Scanned card: " + message_decoded)
        xerox.copy(message_decoded)

# Connect to the broker.
def connect_to_broker():    
    client.connect(broker)
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
