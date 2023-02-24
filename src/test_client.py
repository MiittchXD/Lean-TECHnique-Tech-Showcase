import unittest
import time
from main import Client

class Test(unittest.TestCase):

    # Test variables 
    testName = ""
    testHost = ""
    testPort = ""
    testClientId = ""
    testUsername = ""
    testPassword = ""

    # Instantiate empty Client object
    testClient = Client(testName, testHost, testPort, testClientId, testUsername, testPassword)  

    def test_0_test_connect_valid(self):
        # Set test variables to be valid
        self.testName = 'Test 1'
        self.testHost = 'g7816eb9.ala.us-east-1.emqxsl.com'
        self.testPort = 8883
        self.testClientId = "Test"
        self.testUsername = "LTuser"
        self.testPassword = "password"
        
        # Create valid Client
        self.testClient = Client(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword)
        
        # Run connect function
        self.testClient.connect()

        # Wait for connection
        time.sleep(1)

        # Ensure connect() set client to mqtt Client type
        self.assertEqual(self.testClient.client.is_connected(), True)

        # Disconnect mqtt client
        self.testClient.client.disconnect()

    def test_1_test_connect_invalid(self):
        # Set test variables to be valid
        self.testName = 'Test 2'
        # Set host to invalid to connection force failure
        self.testHost = 'invlid_host_.com'
        self.testPort = 1234
        self.testClientId = "Test"
        self.testUsername = "LTuser"
        self.testPassword = "test"        
        
        # Create invalid Client
        self.testClient = Client(self.testName, self.testHost, self.testPort, self.testClientId, self.testUsername, self.testPassword)
        
        # Run connect function
        self.testClient.connect()

        # Wait for connection
        time.sleep(1)

        # Ensure connect() set client to mqtt Client type
        self.assertEqual(self.testClient.client.is_connected(), False)

        # Disconnect mqtt client
        self.testClient.client.disconnect()



if __name__ == '__main__':
    unittest.main()


       