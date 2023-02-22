#   Project: Lean TECHniques Technical Showcase 
#   Date: 2/22/2023
#   Author: Mitchell Bartoszyk

# Import necessary libraries
import random
import threading
import numpy as np
import time

from paho.mqtt import client as mqtt_client

# Generate semi-random temperature list in range of (68-73), these temp data points will be published to the host by the publisher client
temperatures = np.linspace(68, 73, 20, endpoint=random.randint(0, 1000))

# Host URL, Port, and connection credentials
broker = 'g7816eb9.ala.us-east-1.emqxsl.com'
port = 8883
topic = "temperature"
# generate client ID with pub prefix randomly
client_id_publisher = f'python-mqtt-{random.randint(0, 1000)}'
client_id_subscriber = f'python-mqtt-{random.randint(0, 1000)}'
username = 'LTuser'
password = 'password'

# Simple Fan class to for setting and getting fan state (ON/OFF)
class Fan :
    def __init__(self, state):
        self.fanOn = state

    def setFan(self, state):
        self.fanOn = state

    def getFanState(self):
        return self.fanOn

class publisherThread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
    
    # helper function to execute the threads
    def run(self):
        print("Starting publisherThread...")\

        # Connect publisher client and start publish loop
        publiherClient = connect_mqtt_publisher()
        publiherClient.loop_start()
        publish(publiherClient)
        
class subscriberThread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
 
    # helper function to execute the threads
    def run(self):
        print("Starting subscriberThread...")

        # Connect subscriber client and start listener loop
        subscriberClient = connect_mqtt_subscriber()
        subscribe(subscriberClient)
        subscriberClient.loop_start()

# Function to connect the publisher client to the host
def connect_mqtt_publisher():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Publisher Connected to MQTT Broker!")
        else:
            print("Publisher Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id_publisher)
    client.tls_set()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Function to connect the subscriber client to the host
def connect_mqtt_subscriber() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Subscriber Connected to MQTT Broker!")
        else:
            print("Subscriber Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id_subscriber)
    client.tls_set()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

# Function used by the publisher client to publish a message to the host
def publish(client):
    
    # Maintain message count for use in temperature list indexing
    msg_count = 0

    while msg_count < len(temperatures):
        time.sleep(1)
        # Ensure we loop around once the end of the list is reached
        msg = f"{temperatures[msg_count % len(temperatures)]}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"[PUBLISHER]: Sent `{msg}` to topic `{topic}`")
        else:
            print(f"[PUBLISHER]: Failed to send message to topic {topic}")
        msg_count += 1
    
    # Add extra second of sleep so the last temp published is captured by the Subscriber
    time.sleep(1)

# Function to subscribe the subscrbe client to a topic and set a handler function for when the topic is received
def subscribe(client: mqtt_client):
    
    # Topic message handler
    def on_message(client, userdata, msg):

        temp = msg.payload.decode("utf-8")

        # Set fan on if temp is greater than 70.0 Degrees, otherwise set to false
        if (float(temp) >= 70.0):
           testFan.fanOn = True
        else:
            testFan.fanOn = False
        
        print(f"[SUBSCRIBER]: Current Temperature is `{msg.payload.decode()}' degrees - Fan: {testFan.getFanState()}")
    
    client.subscribe(topic)
    client.on_message = on_message
    


if __name__ == '__main__':
    # Create Publisher and Subscriber threads
    publisher = publisherThread("publisherThread", 0)
    subscriber = subscriberThread("subscriberThread", 1)
    
    # Create Fan object with default status of off (fanOn = False)
    testFan = Fan(False)

    # Start both threads 
    publisher.start()
    subscriber.start()


