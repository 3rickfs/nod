import unittest
import time
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
            result = {'result': json.loads(result.text)["result"]}

            print("__________________________________")
            print(f"result: {result}")
            print("__________________________________")
            print(f"expected_result: {expected_result}")
            #self.assertEqual(expected_result, json.loads(result.text))
            self.assertEqual(expected_result, result)
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

    def test_setting_node_inputs(self):
        print("*"*100)
        print("Test 3: set entire nod inputs to run neurons")
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
        expected_result = {'result': 'nod inputs transferred'}

        try:
            json_data = json.dumps(nod_neurons_input)
            headers = {'Content-type': 'application/json'}
            result = requests.post("http://localhost:5000/save_neurons",
                                   data=json_data, headers=headers
                                  )

            nodo_mem_adr = json.loads(result.text)['nodo_mem_adr']
            #print(res)
            #print(f"res nodo mem adr: {res['nodo_mem_adr']}")

            nod_input = {
                "input_names": ["x1", "x2", "x3", "x4"],
                "inputs": [2, 3, 4, 5],
                "input_idx": [0, 1, 2, 3],
                "nodo_mem_adr": nodo_mem_adr
            }


            json_data = json.dumps(nod_input)
            headers = {'Content-type': 'application/json'}
            result = requests.post("http://localhost:5000/set_nod_inputs",
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

    def test_setting_node_inputs_by_batches(self):
        print("*"*100)
        print("Test 4: set nod inputs by batches to run neurons")
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
        expected_result = []
        expected_result.append('{"result": "nod inputs transferred"}')
        expected_result.append('{"result": "nod inputs transferred"}')
        result = []

        try:
            json_data = json.dumps(nod_neurons_input)
            headers = {'Content-type': 'application/json'}
            res = requests.post("http://localhost:5000/save_neurons",
                                   data=json_data, headers=headers
                                  )

            nodo_mem_adr = json.loads(res.text)['nodo_mem_adr']
            #print(res)
            #print(f"res nodo mem adr: {res['nodo_mem_adr']}")

            nod_input_1 = {
                "input_names": ["x1", "x2", "x3", "x4"],
                "inputs": [4, 5],
                "input_idx": [2, 3],
                "nodo_mem_adr": nodo_mem_adr
            }

            nod_input_2 = {
                "input_names": ["x1", "x2", "x3", "x4"],
                "inputs": [2, 3],
                "input_idx": [0, 1],
                "nodo_mem_adr": nodo_mem_adr
            }

            json_data = json.dumps(nod_input_1)
            headers = {'Content-type': 'application/json'}
            result.append(requests.post("http://localhost:5000/set_nod_inputs",
                                   data=json_data, headers=headers
                                  ).text)
            json_data = json.dumps(nod_input_2)
            result.append(requests.post("http://localhost:5000/set_nod_inputs",
                                   data=json_data, headers=headers
                                  ).text)

            print("__________________________________")
            print(f"result: {result}")
            print("__________________________________")
            print(f"expected_result: {expected_result}")
            self.assertEqual(expected_result, result)
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

    def test_neuron_execution_of_NOD(self):
        print("*"*100)
        print("Test 5: test execution of neurons into a NOD")
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

        output = "[0, 1.2259113788604736]"

        try:
            json_data = json.dumps(nod_neurons_input)
            headers = {'Content-type': 'application/json'}
            res = requests.post("http://localhost:5000/save_neurons",
                                   data=json_data, headers=headers
                                  )

            nodo_mem_adr = json.loads(res.text)['nodo_mem_adr']
            #print(res)
            #print(f"res nodo mem adr: {res['nodo_mem_adr']}")

            nod_input_1 = {
                "input_names": ["x1", "x2", "x3", "x4"],
                "inputs": [4, 5],
                "input_idx": [2, 3],
                "nodo_mem_adr": nodo_mem_adr
            }

            nod_input_2 = {
                "input_names": ["x1", "x2", "x3", "x4"],
                "inputs": [2, 3],
                "input_idx": [0, 1],
                "nodo_mem_adr": nodo_mem_adr
            }

            get_neuron_outputs_input = {
                "nodo_mem_adr": nodo_mem_adr
            }

            json_data = json.dumps(nod_input_1)
            headers = {'Content-type': 'application/json'}
            result = requests.post("http://localhost:5000/set_nod_inputs",
                                   data=json_data, headers=headers
                                  ).text
            json_data = json.dumps(nod_input_2)
            result = requests.post("http://localhost:5000/set_nod_inputs",
                                   data=json_data, headers=headers
                                  ).text
            json_data = json.dumps(get_neuron_outputs_input)
            result = requests.post("http://localhost:5000/get_neuron_outputs",
                                  data=json_data, headers=headers)

            print("__________________________________")
            print(f"result: {result.text}")
            print("__________________________________")
            print(f"expected_result: {output}")
            self.assertEqual(output, result.text)
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

if __name__ == '__main__':
    unittest.main()

