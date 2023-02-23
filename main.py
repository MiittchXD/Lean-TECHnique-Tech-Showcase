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
    
# Create client class
class Client:
    def __init__(self, name, host, port, client_id, username, password):
        self.name = name
        self.host = host
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.client = ""

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"{self.name} Connected to MQTT Broker!")
            else:
                print(f"{self.name} Failed to connect, return code %d\n", rc)
        
        # Create mqtt client and connect, return client object
        client = mqtt_client.Client(self.client_id)
        client.tls_set()
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(broker, port)
        return client

class Publisher(Client):
    def __init__(self, name, host, port, client_id, username, password):
        Client.__init__(self, name, host, port, client_id, username, password)
        self.client = self.connect()

    def publishMsg(self, client):
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

    def start(self):
        self.client.loop_start()
        self.publishMsg(self.client)

class Subscriber(Client):
    def __init__(self, name, host, port, client_id, username, password):
        Client.__init__(self, name, host, port, client_id, username, password)
        self.client = self.connect()

    def subscribe(self, client):
    
        # Topic message handler
        def on_message(client, userdata, msg):

            temp = msg.payload.decode("utf-8")

            # Set fan on if temp is greater than 70.0 Degrees, otherwise set to false
            if (float(temp) >= 70.0):
                testFan.fanOn = True
            else:
                testFan.fanOn = False
            
            print(f"[SUBSCRIBER]: Current Temperature is `{msg.payload.decode()}' degrees - Fan: {testFan.getFanState()}")
        
        # Set topic and set message handler
        self.client.subscribe(topic)
        self.client.on_message = on_message

    def start(self):
        self.subscribe(self.client)
        self.client.loop_start()

class publisherThread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
    
    # helper function to execute the threads
    def run(self):
        print("Starting publisherThread...")\

        # Connect publisher client and start publish loop
        publisher.start()
        
class subscriberThread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
 
    # helper function to execute the threads
    def run(self):
        print("Starting subscriberThread...")

        # Connect subscriber client and start listener loop
        subscriber.start()
    

if __name__ == '__main__':
    
    # Create Publisher and Subscriber objects
    publisher = Publisher("Publisher", broker, port, client_id_publisher, username, password)
    subscriber = Subscriber("Subscriber", broker, port, client_id_subscriber, username, password)

    # Create Publisher and Subscriber threads
    testPublisherThread = publisherThread("publisherThread", 0)
    testPubscriberThread = subscriberThread("subscriberThread", 1)
    
    # Create a basic Fan object with default status of off (fanOn = False)
    testFan = Fan(False)

    # Run both threads 
    testPublisherThread.start()
    testPubscriberThread.start()

    
   
    


