#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# The terminal ID - can be any string.
terminal_id = "T0"

# The broker name or IP address - seller's PC.
#broker = "192.168.56.1"
broker = "server"

# The MQTT client.
client = mqtt.Client()
client.tls_set("/home/szymcio/IOT/main/main/certs/server_client/ca.crt",
    "/home/szymcio/IOT/main/main/certs/server_client/client.crt",
    "/home/szymcio/IOT/main/main/certs/server_client/client.key",
    tls_version=2)

# Connect to the broker.
def connect_to_broker():
    client.connect(broker, port=8883)
    # Send message about conenction.
    notify_server(True)


def disconnect_from_broker():
    # Send message about disconenction.
    notify_server(False)
    # Disconnet the client.
    client.disconnect()

def call_worker(card_id):
    client.publish("seller/terminal", card_id)
    #print("Scanned card " + card_id)

def notify_server(connected):
    if connected:
        client.publish("seller/connections", f"{terminal_id}.connected")
    else:
        client.publish("seller/connections", f"{terminal_id}.disconnected")

def run_sender():
    connect_to_broker()
    client.loop_start()

    while(client.is_connected):
        id = input()
        call_worker(id)

    #disconnect_from_broker()


if __name__ == "__main__":
    run_sender()
