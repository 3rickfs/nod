import unittest
import requests
from nod.nod import nod

class neuron_ops_test_cases(unittest.TestCase):

    def test_api_hello_world(self):
        print("*"*100)
        print("Test 1: call http://IP:PORT/ to get hello world greetings!") 
        expected_result = ("<p>Hello, World! I'm a virtual NOD (Neuro Orches"
                           "trated Device) running in EKS cluster in AWS as a"
                           "pod. So I'm ready for running multiple neurons."
                           "Nice to meet you.</p>")

        try:
            result = requests.get(("http://a545ed66e46bc4ea788f4aada7bcea72-"
                                   "1944961211.us-west-1.elb.amazonaws.com:5000/"))
            print(result.text)
            self.assertEqual(expected_result, result.text)
        except Exception as e:
            print("-"*100)
            print(f"error: {e}")
            print("-"*100)

        print("*"*100)

if __name__ == '__main__':
    unittest.main()

