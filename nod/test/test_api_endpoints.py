import unittest
import requests
import json

from nod.nod import nod

class neuron_ops_test_cases(unittest.TestCase):

    def test_api_hello_world(self):
        print("*"*100)
        print("Test 1: call http://IP:PORT/ to get hello world greetings!") 
        expected_result = ("<p>Hello, World! I'm a virtual NOD (Neuro Orches"
                           "trated Device) running in EKS cluster in AWS as a"
                           " pod. So I'm ready for running multiple neurons."
                           " Nice to meet you.</p>")

        try:
            result = requests.get(("http://a545ed66e46bc4ea788f4aada7bcea72-"
                                   "1944961211.us-west-1.elb.amazonaws.com:5000/"))
            print(result.text)
            print(expected_result)
            self.assertEqual(expected_result, result.text)
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

    def test_model_json_to_neuron_set_jsons(self):
        print("*"*100)
        print("Test 2: call http://IP:PORT/model_to_neuron_sets to split the"
               "whole model in json into group of neurons in json too.")
        input_file_name = "json-modelo-ia.json"
        CoN_parameters = {
            "neurons_per_nod": 2,
            "nod_num": 10
        }
        expected_result = {
            "nod_1": {
                "nod_id": "1",
                "capa_id": "1",
                "input_names": ['x1', 'x2', 'x3', 'x4'],
                "pesos": [[-0.35309315, -0.2911589, -0.23536563, -0.3734181],
                          [0.7257507, -0.6246722, -0.70658255, 0.63884974]
                         ],
                "biases": [0, 0],
                "fas": ['relu', 'relu'],
                "output_names": ['o1', 'o2'],
                "output_ep":[("http://a6823b10e5c7a4dd5a038a6f813091b4-"
                              "242539242.us-west-1.elb.amazonaws.com:5000/"
                              "exec_neurons"),
                             ("http://a6823b10e5c7a4dd5a038a6f813091b4-"
                              "242539242.us-west-1.elb.amazonaws.com:5000/"
                              "exec_neurons")
                            ]
            },
            "nod_2": {
                "nod_id": "2",
                "capa_id": "2",
                "input_names": ['o1', 'o2'],
                "pesos": [[0.2804066, 0.4414947],
                          [-0.68139964, -0.5475711]
                         ],
                "biases": [0, 0],
                "fas": ['relu', 'relu'],
                "output_names": ['o3', 'o4'],
                "output_ep":[("http://a545ed66e46bc4ea788f4aada7bcea72-",
                              ":1944961211.us-west-1.elb.amazonaws.com:5000/"
                              "model_output"),
                             ("http://a545ed66e46bc4ea788f4aada7bcea72-",
                              ":1944961211.us-west-1.elb.amazonaws.com:5000/"
                              "model_output")
                            ]
            }
        }

        try:
            with open(input_file_name, 'rb') as jf:
                input_json_file = json.load(jf)
            print(f"json file: {input_json_file}")
            #adding parameters of Cluster of Neurons
            input_json_file["CoN_parameters"] = CoN_parameters
            json_data = json.dumps(input_json_file)
            headers = {'Content-type': 'application/json'}
            result = requests.post("http://localhost:5000/model_to_neuron_sets",
                                   data=json_data, headers=headers
                                  )

            print("__________________________________")
            print(f"result: {json.loads(result.text)}")
            print("__________________________________")
            print(f"expected_result: {expected_result}")
            self.assertEqual(expected_result, result.text)
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

if __name__ == '__main__':
    unittest.main()

