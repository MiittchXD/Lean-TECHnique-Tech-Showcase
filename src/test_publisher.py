import unittest
import time
from main import Publisher

class Test(unittest.TestCase):

    # Test variables
    testTopic = ""
    testMessages = []

    # Valid MQTT Client info 
    testName = 'Test'
    testHost = 'g7816eb9.ala.us-east-1.emqxsl.com'
    testPort = 8883
    testClientId = "Test"
    testUsername = "LTuser"
    testPassword = "password"


    # Instantiate empty Client object
    testPublisher = ""

    def test_0_test_publish_valid_message(self):
        
        self.testName = "Test 1" 

        # Set test variables to be valid
        self.testMessages = [1, 2, 3, 4, 5]
        self.testTopic = "TestTopic"
        
        # Create valid Publisher which then auto-connects the mqtt client
        self.testPublisher = Publisher(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword, self.testMessages)  

        # Publish messages
        numSent = self.testPublisher.publishMsg(self.testPublisher.client, self.testTopic, self.testPublisher.messages)

        # Ensure all messages sent
        self.assertEqual(numSent, len(self.testMessages))

        # Disconnect mqtt client
        self.testPublisher.client.disconnect()

    def test_1_test_publish_invalid_message(self):

        self.testName = "Test 2" 
        
        # Valid topic and invalid messages
        self.testMessages = str
        self.testTopic = "TestTopic"

        # Create valid Publisher which then auto-connects the mqtt client
        self.testPublisher = Publisher(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword, self.testMessages)  
        self.testPublisher.connect()

        # Publish messages
        numSent = self.testPublisher.publishMsg(self.testPublisher.client, self.testTopic, self.testPublisher.messages)

        # Ensure invalid message was not sent
        self.assertEqual(numSent, 0)

        # Disconnect mqtt client
        self.testPublisher.client.disconnect()

    def test_2_test_publish_invalid_topic(self):

        self.testName = "Test 3"

        # Valid messages and invalid topic
        self.testMessages = [1, 2, 3, 4, 5]
        self.testTopic = ""

        # Create valid Publisher which then auto-connects the mqtt client
        self.testPublisher = Publisher(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword, self.testMessages)  
        self.testPublisher.connect()

        # Publish messages
        numSent = self.testPublisher.publishMsg(self.testPublisher.client, self.testTopic, self.testPublisher.messages)

        # Ensure invalid message was not sent
        self.assertEqual(numSent, 0)

        # Disconnect mqtt client
        self.testPublisher.client.disconnect()

    def test_3_test_set_topic_valid(self):

        self.testName = "Test 4"

        test_topic = "Valid"
        
        # Create valid Publisher which then auto-connects the mqtt client
        self.testPublisher = Publisher(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword, self.testMessages)  

        self.testPublisher.setTopic(test_topic)

        self.assertEqual(self.testPublisher.topic, test_topic)

    def test_4_test_set_topic_valid_type_invalid_value(self):

        self.testName = "Test 5"
        
        # Create valid Publisher which then auto-connects the mqtt client
        self.testPublisher = Publisher(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword, self.testMessages)  

        old_topic = self.testPublisher.topic

        test_topic = ""

        self.testPublisher.setTopic(test_topic)

        self.assertEqual(self.testPublisher.topic, old_topic)

    def test_5_test_set_topic_invalid_type(self):

        self.testName = "Test 6"

        self.testPublisher = Publisher(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword, self.testMessages)  

        self.testPublisher.setTopic("Valid")

        old_topic = self.testPublisher.topic

        test_topic = 2

        self.testPublisher.setTopic(test_topic)

        self.assertEqual(self.testPublisher.topic, old_topic)

    
if __name__ == '__main__':
    unittest.main()