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
        
        if (type(state) is not type(True)):
            # Invalid state detected, do not change state
            print("[setFan]: Invalid state! No change.\n")

            return
        else:
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
                print(f"{self.name} Connected to MQTT Broker!\n")
            else:
                print(f"\n{self.name} Failed to connect, return code", rc)
        
        # Create mqtt client and connect, return client object
        client = mqtt_client.Client(self.client_id)
        client.tls_set()
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(broker, port)
        self.client = client

        self.client.loop_start()
        
        return client

class Publisher(Client):
    def __init__(self, name, host, port, client_id, username, password, messages):
        Client.__init__(self, name, host, port, client_id, username, password)
        self.messages = messages
        self.client = self.connect()
        self.topic = ""

    def setTopic(self, topic):
        if (type(topic) == type("")):
            if (len(topic) > 0):
                self.topic = topic
                return True
            else:
                return False
        else:
            return False

    def publishMsg(self, client, topic_to_send, messages):
        # Maintain message count for use in temperature list indexing
        msg_count = 0

        try:
            length = len(messages)
        except:
            return msg_count
        
        if topic_to_send == "":
            return msg_count

        while msg_count < len(messages):
            time.sleep(1)
            # Ensure we loop around once the end of the list is reached
            msg = f"{messages[msg_count % len(messages)]}"
            result = client.publish(topic_to_send, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"[PUBLISHER]: Sent `{msg}` to topic `{topic_to_send}`")
                msg_count += 1
            else:
                print(f"[PUBLISHER]: Failed to send message to topic {topic_to_send}")
        
        # Add extra second of sleep so the last temp published is captured by the Subscriber
        time.sleep(1)

        return msg_count

class Subscriber(Client, Fan):
    def __init__(self, name, host, port, client_id, username, password):
        Client.__init__(self, name, host, port, client_id, username, password)
        Fan.__init__(self, False)
        self.client = self.connect()
        self.numReceived = 0
        self.topic = ""

    def setTopic(self, topic):
        if (type(topic) == type("")):
            if (len(topic) > 0):
                self.topic = topic
                return True
            else:
                return False
        else:
            return False

    def subscribe(self, client):

        if ((self.topic == "") or (type(self.topic) is not type(""))):
            print("[subcribe]: Invalid topic!")
            return False
    
        # Topic message handler
        def on_message(client, userdata, msg):

            self.numReceived += 1

            temp = msg.payload.decode("utf-8")

            # Set fan on if temp is greater than 70.0 Degrees, otherwise set to false
            if (float(temp) >= 70.0):
                self.fanOn = True
            else:
                self.fanOn = False
            
            print(f"[SUBSCRIBER]: Current Temperature is `{msg.payload.decode()}' degrees - Fan: {self.getFanState()}")
        
        # Set topic and set message handler
        self.client.subscribe(self.topic)
        self.client.on_message = on_message
        return True

class publisherThread(threading.Thread):
    def __init__(self, thread_name, thread_ID, publisher):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.publisher = publisher
    
    # helper function to execute the threads
    def run(self):
        print("Starting Publisher Thread...")\
        
        # Start publish loop
        self.publisher.publishMsg(self.publisher.client, self.publisher.topic, self.publisher.messages)
        
class subscriberThread(threading.Thread):
    def __init__(self, thread_name, thread_ID, subscriber):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.subscriber = subscriber

    # helper function to execute the threads
    def run(self):
        print("Starting Subscriber Thread...")

        # Call subscribe function to start listening for temptopic message
        self.subscriber.subscribe(self.subscriber.client)
    

if __name__ == '__main__':
    
    # Create Publisher and Subscriber objects
    publisher = Publisher("Publisher", broker, port, client_id_publisher, username, password, temperatures)
    subscriber = Subscriber("Subscriber", broker, port, client_id_subscriber, username, password)

    # Add topic to subscriber
    subscriber.setTopic(topic)
    publisher.setTopic(topic)

    # Create Publisher and Subscriber threads
    testPublisherThread = publisherThread("publisherThread", 0, publisher)
    testPubscriberThread = subscriberThread("subscriberThread", 1, subscriber)

    # Run both threads 
    testPublisherThread.start()
    testPubscriberThread.start()

    
   
    


