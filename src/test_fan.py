import unittest
from main import Fan

# This is the class we want to test. So, we need to import it

class Test(unittest.TestCase):

    # Instantiate Fan object
    testFan = Fan(False)  

    # test case function to check the Person.set_name function
    def test_0_set_state_false(self):

        # Set to True to ensure setting to False works
        self.testFan.fanOn = True

        # Call setFan() with False
        self.testFan.setFan(False)

        self.assertEqual(self.testFan.fanOn, False)

    def test_1_set_state_true(self):

        # Set to False to ensure setting to True works 
        self.testFan.fanOn = False

        # Call setFan() with True
        self.testFan.setFan(True)

        self.assertEqual(self.testFan.fanOn, True)

    def test_2_set_state_invalid_type(self):
        
        # Set fan state to True and make sure it is not changed once an invalid state is attempted
        self.testFan.fanOn = True

        # Call setFan() with invalid type
        self.testFan.setFan("False")

        self.assertEqual(self.testFan.fanOn, True)


    def test_3_get_fan_state(self):
        
       # Set fan state to False
       self.testFan.fanOn = False

       self.assertEqual(self.testFan.getFanState(), False)

       # Set fan state to True
       self.testFan.fanOn = True

       self.assertEqual(self.testFan.getFanState(), True)



if __name__ == '__main__':
    unittest.main()


       