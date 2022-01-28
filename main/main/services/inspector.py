#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter as tk
import time
import xerox

WIDTH = 600
HEIGHT = 480

# The terminal ID - can be any string.
terminal_id = "T0"

# MQTT and GUI are in the same file because of MQTT messages updates main window (which is the only window),
# and therefore "on_message" has to be executed in main thread

#------------- MQTT----------------

# The broker name or IP address - server.
#broker = "192.168.56.1"
broker = "server"

# The MQTT client.
client = mqtt.Client()
client.tls_set("D:\Studia\IoT\projekt repo\IOT\main\main\certs\inspector\ca.crt",
    "D:\Studia\IoT\projekt repo\IOT\main\main\certs\inspector\client.crt",
    "D:\Studia\IoT\projekt repo\IOT\main\main\certs\inspector\client.key",
    tls_version=2)

# Process message received from server
def process_message(client, userdata, message):
    global timer
    root.after_cancel(timer)

    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")

    # Valid ticket
    if message_decoded[0] == '4':
        show_card_info(**{'Imię' : message_decoded[1], 'Nazwisko' : message_decoded[2], 'Status':"Ważny", "Ważny do" : message_decoded[3]})
    # Expired ticket
    elif message_decoded[0] == '3':
        show_card_info(**{'Imię' : message_decoded[1], 'Nazwisko' : message_decoded[2], 'Status':"Nieważny!", "Ważny do" : message_decoded[3]})
    # No ticket
    elif message_decoded[0] == '2':
        show_card_info(**{'Imię' : message_decoded[1], 'Nazwisko' : message_decoded[2], 'Status':"Brak biletu!"})
    # Card is not active
    elif message_decoded[0] == '1':
        show_card_info(**{'Status':"Nieaktywna!"})
    # No such card in database
    elif message_decoded[0] == '0':
        show_card_info(**{'Status':"Brak karty w systemie!"})

# Publish a message with number of scanned card
def call_worker():
    client.publish(f"terminal/scanned", terminal_id + "." + xerox.paste())

# Notifying about connection/disconnection
def notify_server(connected):
    if connected:   
        client.publish("terminal/connections", f"{terminal_id}.connected")
    else:
        client.publish("terminal/connections", f"{terminal_id}.disconnected")

# Connect to the broker.
connect_flag = False
def connect_to_broker():
    global connect_flag
    try:
        client.connect(broker, port=8883)
        client.subscribe(f"server/{terminal_id}")
        client.on_message = process_message
        # Send message about connection.
        notify_server(True)
        connect_flag = True
    except TimeoutError:
        show_connection_failed()
        connect_flag = False

        

def disconnect_from_broker():
    # Send message about disconenction.
    notify_server(False)
    # Disconnet the client.
    client.disconnect()

#------------------- GUI -----------------

# The main window.
root = tk.Tk()

# Last screen showing info about ticket, its owner and button to come back to first screen
def show_card_info(**kwargs):
    frame = root.winfo_children()[0].winfo_children()[0]
    clean_widget(frame)

    curr_rely = 0

    for key, value in kwargs.items():
        name_label = tk.Label(frame, text=f"{key}:")
        name_label.place(relx=0, rely=curr_rely, relwidth=0.45, relheight=0.1)

        name_value = tk.Label(frame, text=value)
        name_value.place(relx=0.5, rely=curr_rely, relwidth=0.45, relheight=0.1)

        curr_rely += 0.15

    return_btn = tk.Button(frame, text="Powrót", command=show_main)
    return_btn.place(relx=0.375, rely=curr_rely+0.05, relwidth=0.25, relheight=0.15)

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
        call_worker()
        first_time = None

def handler_keyreleased(event):
    global first_time
    first_time = None


# Screen showing client hasn't received message from server
def show_no_response():
    frame = root.winfo_children()[0].winfo_children()[0]
    clean_widget(frame)

    label_failed = tk.Label(frame, text="Brak odpowiedzi od serwera!")
    label_failed.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.1)

    label_retry = tk.Label(frame, text="Spróbuj zeskanować jeszcze raz.")
    label_retry.place(relx=0.05, rely=0.35, relwidth=0.9, relheight=0.1)

    return_btn = tk.Button(frame, text="Powrót", command=show_main)
    return_btn.place(relx=0.375, rely=0.45, relwidth=0.25, relheight=0.1)

timer = ""
# Screen showing confirmation of the scan and an ask for waiting.
def show_waiting():
    global timer
    frame = root.winfo_children()[0].winfo_children()[0]
    clean_widget(frame)

    label = tk.Label(frame, text="Zeskanowano kartę. Proszę czekać")
    label.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)
    timer = root.after(2000, show_no_response)

# Screen showing connection failed and asking for retry.
def show_connection_failed():
    root.title("TERMINAL")
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(canvas)
    frame.place(relx=0.07, rely=0.07, relwidth=0.86, relheight=0.86)

    label_failed = tk.Label(frame, text="Nie można połączyć się z serwerem!")
    label_failed.place(relx=0.05, rely=0.3, relwidth=0.9, relheight=0.1)

    label_retry = tk.Label(frame, text="Spróbuj ponownie później.")
    label_retry.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.1)

# Substitute of event handler but for entries and buttons
def after_scanned(card_id):
    for char in card_id:
        if not char.isdigit():
            return
    call_worker(card_id)
    show_waiting()

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

    if connect_flag:
        create_main_window()
        client.loop_start()

    # Start to display window (It will stay here until window is displayed)
    root.mainloop()

    disconnect_from_broker()


if __name__ == "__main__":
    run_sender()
