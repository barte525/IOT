#!/usr/bin/env python3

from django.http import response
import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time
import requests

# The broker name or IP address - this machine.
broker = "server"
#broker = "192.168.56.1"

# The MQTT client.
client = mqtt.Client()
client.tls_set("/home/szymcio/IOT/main/main/certs/server_client/ca.crt",
    "/home/szymcio/IOT/main/main/certs/server_client/client.crt",
    "/home/szymcio/IOT/main/main/certs/server_client/client.key",
    tls_version=2)

# Processing message from seller terminal depending on the topic (connections vs scanned cards)
# TODO Selecting ticket info from database in 'else' part of if-else statement
def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(".")

    # Info about connected devices and subscribing to topic related to given terminal.
    if message.topic == "terminal/connections":
        print(message_decoded[0] + " : " + message_decoded[1])
    # Printing which card was scanned and sending info to terminal
    else:
        print(f"{time.ctime()}, terminal: {message_decoded[0]} scanned card {message_decoded[1]}")
        #Hard-coded info about scanned card - "name, surname, valid to"
        response = requests.get(f"http://127.0.0.1:8000/api/czy_aktywna/{message_decoded[1]}").json()

        if(response['opis'] == 4 or response["opis"] == 3):
            client.publish(f"server/{message_decoded[0]}", f"{response['opis']},{response['imie']},{response['nazwisko']},{response['termin']}")

        elif response['opis'] == 2: 
            client.publish(f"server/{message_decoded[0]}", f"{response['opis']},{response['imie']},{response['nazwisko']}")
            
        elif response['opis'] == 1 or response['opis'] == 0:
            client.publish(f"server/{message_decoded[0]}", f"{response['opis']}")


# Connect to the broker.
def connect_to_broker():
    client.connect(broker, port=8883)
    client.on_message = process_message
    client.on_disconnect = disconnect_from_broker
    # Starts client and subscribe.
    client.subscribe("terminal/connections")
    client.subscribe("terminal/scanned")
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
