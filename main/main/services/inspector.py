#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter as tk
import time

WIDTH = 600
HEIGHT = 480

# The terminal ID - can be any string.
terminal_id = "T0"

# MQTT and GUI are in the same file because of MQTT messages updates main window (which is the only window),
# and therefore "on_message" has to be executed in main thread

#------------- MQTT----------------

# The broker name or IP address - server.
broker = "192.168.56.1"
#broker = "localhost"
# The MQTT client.
client = mqtt.Client()

# Process message received from server
def process_message(client, userdata, message):

    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")

    date = time.strptime(message_decoded[2], "%d/%m/%Y %H:%M")
    # Update view after 2000ms (2s) to simulate waiting for response
    if date > time.strptime(time.strftime("%d/%m/%Y %H:%M"), "%d/%m/%Y %H:%M"):
        root.after(2000, show_card_info, message_decoded[0], message_decoded[1], True, message_decoded[2])
    else:
        root.after(2000, show_card_info, message_decoded[0], message_decoded[1], False, message_decoded[2])

# Publish a message with number of scanned card
def call_worker(card_id):
    client.publish(f"terminal/{terminal_id}", terminal_id + "." + card_id)

# Notifying about connection/disconnection
def notify_server(connected):
    if connected:   
        client.publish("terminal/connections", f"{terminal_id}.connected")
    else:
        client.publish("terminal/connections", f"{terminal_id}.disconnected")

# Connect to the broker.
def connect_to_broker():
    client.connect(broker)
    client.subscribe(f"server/{terminal_id}")
    client.on_message = process_message
    # Send message about connection.
    notify_server(True)


def disconnect_from_broker():
    # Send message about disconenction.
    notify_server(False)
    # Disconnet the client.
    client.disconnect()

#------------------- GUI -----------------

# The main window.
root = tk.Tk()

# Last screen showing info about ticket, its owner and button to come back to first screen
def show_card_info(name, surname, valid, validTo):
    frame = root.winfo_children()[0].winfo_children()[0]
    clean_widget(frame)

    name_label = tk.Label(frame, text="Imię:")
    name_label.place(relx=0, rely=0, relwidth=0.45, relheight=0.1)

    name_value = tk.Label(frame, text=name)
    name_value.place(relx=0.5, rely=0, relwidth=0.45, relheight=0.1)

    surname_label = tk.Label(frame, text="Nazwisko:")
    surname_label.place(relx=0, rely=0.15, relwidth=0.45, relheight=0.1)

    surname_value = tk.Label(frame, text=surname)
    surname_value.place(relx=0.5, rely=0.15, relwidth=0.45, relheight=0.1)

    valid_date = tk.Label(frame, text="Ważna do:")
    valid_date.place(relx=0, rely=0.3, relwidth=0.45, relheight=0.1)

    valid_date_value = tk.Label(frame, text=validTo)
    valid_date_value.place(relx=0.5, rely=0.3, relwidth=0.45, relheight=0.1)

    correct = tk.Label(frame, text="Status:")
    correct.place(relx=0, rely=0.45, relwidth=0.45, relheight=0.1)

    if valid:
        correct_value = tk.Label(frame, text="Ważny")
        correct_value.place(relx=0.5, rely=0.45, relwidth=0.45, relheight=0.1)
    else:
        correct_value = tk.Label(frame, text="Nieważny!")
        correct_value.place(relx=0.5, rely=0.45, relwidth=0.45, relheight=0.1)

    return_btn = tk.Button(frame, text="Powrót", command=show_main)
    return_btn.place(relx=0.375, rely=0.65, relwidth=0.25, relheight=0.15)

# Handling event simulating scanning card - hold key for more than 2 seconds
# If you want to use it - uncomment "bind" lines and comment lines with id_input, id_btn in show_main
first_time = None
def handler_keypressed(event):
    if not event.char.isdigit():
        return

    global first_time

    if first_time == None:
        first_time = event.time
    elif event.time - first_time > 2000:
        root.unbind("<Key>")
        root.unbind("<KeyRelease>")
        show_waiting()
        call_worker(event.char)

def handler_keyreleased(event):
    global first_time
    first_time = None

# Screen showing confirmation of the scan and an ask for waiting.
def show_waiting():
    frame = root.winfo_children()[0].winfo_children()[0]
    clean_widget(frame)

    label = tk.Label(frame, text="Zeskanowano kartę. Proszę czekać")
    label.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

# Substitute of event handler but for entries and buttons
def after_scanned(card_id):
    for char in card_id:
        if not char.isdigit():
            return
    show_waiting()
    call_worker(card_id)

# Main window and frame
def create_main_window():
    root.title("TERMINAL")
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(canvas)
    frame.place(relx=0.07, rely=0.07, relwidth=0.86, relheight=0.86)

    show_main()

# Removing every children of given widget
def clean_widget(widget):
    if len(widget.winfo_children()) > 0:
        for item in widget.winfo_children():
            item.destroy()

# First screen - waiting for card
def show_main():
    # Binding event handler on key press
    root.bind("<Key>", handler_keypressed)
    root.bind("<KeyRelease>", handler_keyreleased)

    frame = root.winfo_children()[0].winfo_children()[0]

    clean_widget(frame)

    intro_label = tk.Label(frame, text="Proszę przyłożyć kartę:")
    intro_label.place(relx=0.05, rely=0.375, relwidth=0.9, relheight=0.25)

    #id_input = tk.Entry(frame)
    #id_input.place(relx=0.20, rely=0.3, relwidth=0.4, relheight=0.1)

    #id_btn = tk.Button(frame, text="Skanuj", command=lambda: after_scanned(id_input.get()))
    #id_btn.place(relx=0.60, rely=0.3, relwidth=0.2, relheight=0.1)


def run_sender():
    connect_to_broker()
    create_main_window()

    
    client.loop_start()
    # Start to display window (It will stay here until window is displayed)
    root.mainloop()

    disconnect_from_broker()


if __name__ == "__main__":
    run_sender()
