#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time

# The broker name or IP address - this machine.
broker = "server"
#broker = "192.168.56.1"

# The MQTT client.
client = mqtt.Client()
client.tls_set("main\main\certs\ca.crt",tls_version=2)

# Processing message from seller terminal depending on the topic (connections vs scanned cards)
# TODO Selecting ticket info from database in 'else' part of if-else statement
def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")

    # Info about connected devices and subscribing to topic related to given terminal.
    if message.topic == "terminal/connections":
        print(message_decoded[0] + " : " + message_decoded[1])
        if(message_decoded[1] == "connected"):
            client.subscribe(f"terminal/{message_decoded[0]}")
    # Printing which card was scanned and sending info to terminal
    else:
        print(f"{time.ctime()}, terminal: {message_decoded[0]} scanned card {message_decoded[1]}")
        #Hard-coded info about scanned card - "name, surname, valid to"
        client.publish(f"server/{message_decoded[0]}", "Jadwiga,Hymel,08/01/2022 17:32")


# Connect to the broker.
def connect_to_broker():
    client.connect(broker, port=8883)
    client.on_message = process_message
    client.on_disconnect = disconnect_from_broker
    # Starts client and subscribe.
    client.subscribe("terminal/connections")
    client.loop_forever()

# Disconnet the client.
def disconnect_from_broker():
    # client.loop_stop()
    client.disconnect()


def run_receiver():
    connect_to_broker()
    #disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
