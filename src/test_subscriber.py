import unittest
import time
from main import Subscriber
from main import Publisher
from main import publisherThread
from main import subscriberThread
from main import Fan

class Test(unittest.TestCase):

    # Test variables
    testTopic = "valid"
    testMessages = [1, 2, 3, 4, 5]

    # Valid MQTT Client info 
    testName = 'Test'
    testHost = 'g7816eb9.ala.us-east-1.emqxsl.com'
    testPort = 8883
    testClientId = "Test"
    testUsername = "LTuser"
    testPassword = "password"

    # Instantiate empty Client object
    testSubscriber = "" 
    testPublisher = ""

    def test_0_test_set_valid_topic(self):

        self.testSubscriber = Subscriber(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword)
        
        # Wait for mqtt client connection
        time.sleep(1)

        # Set to valid Topic
        testTopic = "ValidTopic"
        set = self.testSubscriber.setTopic(testTopic)

        # Verify setTopic returns true with valid topic
        self.assertEqual(set, True)

        # Verify setTopic sets Publisher topic variable
        self.assertEqual(self.testSubscriber.topic, testTopic)

        # Disconnect mqtt client
        self.testSubscriber.client.disconnect()

    def test_1_test_set_topic_valid_type_invalid_topic(self):

        self.testSubscriber = Subscriber(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword)
        
        # Wait for mqtt client connection
        time.sleep(1)

        # Save current topic to ensure it isn't changed when invalid topic is used with setTopic()
        oldtestTopic = self.testSubscriber.topic
        testTopic = ""

        set = self.testSubscriber.setTopic(testTopic)

        # Verify setTopic returns true with valid topic
        self.assertEqual(set, False)

        # Verify setTopic sets Publisher topic variable
        self.assertEqual(self.testSubscriber.topic, oldtestTopic)

        # Disconnect mqtt client
        self.testSubscriber.client.disconnect()

    def test_2_test_set_topic_invalid_type(self):

        self.testSubscriber = Subscriber(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword)
        
        # Wait for mqtt client connection
        time.sleep(1)

        # Save current topic to ensure it isn't changed when invalid topic is used with setTopic()
        oldtestTopic = self.testSubscriber.topic
        testTopic = 2

        set = self.testSubscriber.setTopic(testTopic)

        # Verify setTopic returns true with valid topic
        self.assertEqual(set, False)

        # Verify setTopic sets Publisher topic variable
        self.assertEqual(self.testSubscriber.topic, oldtestTopic)

        # Disconnect mqtt client
        self.testSubscriber.client.disconnect()

    def test_3_test_subscribe_valid_topic(self):

        self.testSubscriber = Subscriber(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword)
        
        # Wait for mqtt client connection
        time.sleep(1)
        
        # Set valid topic
        self.testSubscriber.setTopic("ValidTopic")

        subscribed = self.testSubscriber.subscribe(self.testSubscriber.client)

        # Verify setTopic returns true with valid topic
        self.assertEqual(subscribed, True)

        self.testSubscriber.client.disconnect()

    def test_4_test_subscribe_invalid_topic(self):

        self.testSubscriber = Subscriber(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword)
        
        # Wait for mqtt client connection
        time.sleep(1)
        
        # Set invalid topic
        self.testSubscriber.setTopic("")

        subscribed = self.testSubscriber.subscribe(self.testSubscriber.client)

        # Verify setTopic returns true with valid topic
        self.assertEqual(subscribed, False)

        # Set invalid topic
        self.testSubscriber.setTopic(4)

        subscribed = self.testSubscriber.subscribe(self.testSubscriber.client)

        # Verify setTopic returns true with valid topic
        self.assertEqual(subscribed, False)

        self.testSubscriber.client.disconnect()

    def test_5_test_subscribe_test_numReceived(self):

        valid_messages = [1, 2, 3, 4, 5]

        # Create Publisher and Subscriber objects
        publisher = Publisher(self.testName, self.testHost, self.testPort, "pub_client", self.testUsername, self.testPassword, valid_messages)
        subscriber = Subscriber(self.testName, self.testHost, self.testPort, "sub_client", self.testUsername, self.testPassword)

        # Add topic to subscriber
        subscriber.setTopic("Test")
        publisher.setTopic("Test")

        # Wait for connection 
        time.sleep(1)

        # Create Publisher and Subscriber threads
        testPublisherThread = publisherThread("publisherThread", 0, publisher)
        testPubscriberThread = subscriberThread("subscriberThread", 1, subscriber)

        # Run both threads 
        testPublisherThread.start()
        testPubscriberThread.start()
        
        # Wait for both threads to run
        while (testPublisherThread.is_alive() or testPubscriberThread.is_alive()):
            time.sleep(1)

        # Assert all messages were received and count was updated
        self.assertEqual(subscriber.numReceived, len(publisher.messages))

        # Disconnect both mqtt clients
        publisher.client.disconnect()
        subscriber.client.disconnect()

    def test_6_test_subscribe_test_numReceived_diff_topic(self):

        valid_messages = [1, 2, 3, 4, 5]

        # Create Publisher and Subscriber objects
        publisher = Publisher(self.testName, self.testHost, self.testPort, "pub_client", self.testUsername, self.testPassword, valid_messages)
        subscriber = Subscriber(self.testName, self.testHost, self.testPort, "sub_client", self.testUsername, self.testPassword)

        # Add topic to subscriber
        subscriber.setTopic("Test")
        publisher.setTopic("Other")

        # Wait for connection 
        time.sleep(1)

        # Create Publisher and Subscriber threads
        testPublisherThread = publisherThread("publisherThread", 0, publisher)
        testPubscriberThread = subscriberThread("subscriberThread", 1, subscriber)

        # Run both threads 
        testPublisherThread.start()
        testPubscriberThread.start()
        
        # Wait for both threads to run
        while (testPublisherThread.is_alive() or testPubscriberThread.is_alive()):
            time.sleep(1)

        # Assert that no messages were received since none with the subscribers topic were sent by the publisher
        self.assertEqual(subscriber.numReceived, 0)

        publisher.client.disconnect()
        subscriber.client.disconnect()

if __name__ == '__main__':
    unittest.main()