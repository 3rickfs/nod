import unittest
import requests
import json

from nod.nod import nod

class neuron_ops_test_cases(unittest.TestCase):
    def test_api_hello_world(self):
        print("*"*100)
        print("Test 1: call http://localhost:5000/ to get hello world greetings from"\
              "a node running in an EKS cluster!")
        print("-------------------------------------------------------------")
        expected_result = ("<p>Hello, World! I'm a virtual NOD (Neuro Orches"
                           "trated Device) running in EKS cluster in AWS as a"
                           " pod. So I'm ready for running multiple neurons."
                           " Nice to meet you.</p>")

        try:
            result = requests.get("http://localhost:5000/")
            print("__________________________________")
            print(f"result: {result.text}")
            print("__________________________________")
            print(f"expected_result: {expected_result}")
            self.assertEqual(expected_result, result.text)
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)


    def test_read_nod_paramaters(self):
        print("*"*100)
        print("Test 2: test read_paramaters method of nod objects")
        print("-------------------------------------------------------------")
        nod_neurons_input =  {
            'nod_id': '1',
            'capa_id': '1',
            'input_names': ['x1', 'x2', 'x3', 'x4'],
            'pesos': [
                [-0.4397721290588379,
                 -0.8503506183624268,
                 0.11941719055175781,
                 0.28388309478759766],
                [-0.8684360980987549,
                 -0.2745087146759033,
                 0.3909769058227539,
                 0.44448041915893555]
            ],
            'biases': [0.0, 0.0],
            'fas': ['relu', 'relu'],
            'output_names': ['o1', 'o2'],
            'output_ep': ['http://nod3:5000/exec_neurons',
                          'http://nod3:5000/exec_neurons'
                         ]
        }

        expected_result = {'result': 'neurons installed'}

        try:
            json_data = json.dumps(nod_neurons_input)
            headers = {'Content-type': 'application/json'}
            result = requests.post("http://localhost:5000/save_neurons",
                                   data=json_data, headers=headers
                                  )

            print("__________________________________")
            print(f"result: {json.loads(result.text)}")
            print("__________________________________")
            print(f"expected_result: {expected_result}")
            self.assertEqual(expected_result, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

if __name__ == '__main__':
    unittest.main()

