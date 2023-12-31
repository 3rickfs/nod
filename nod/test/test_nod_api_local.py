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

    def test_neuron_execution_of_two_NODs(self):
        print("*"*100)
        print("Test 5: test execution of neurons in two NODs.")
        print("First distributed AI model running in local.")
        print("-------------------------------------------------------------")

        nod_1_neurons_input =  {
            'nod_id': '1',
            'capa_id': '1',
            'input_names': ['x1', 'x2', 'x3', 'x4'],
            'pesos': [
                [-0.35309315, -0.2911589, -0.23536563, -0.3734181],
                [0.7257507, -0.6246722, -0.70658255, 0.63884974]
            ],
            'biases': [0.0, 0.0],
            'fas': ['relu', 'relu'],
            'output_names': ['o1', 'o2'],
            #TODO: endpoint seems like to be done again considering all
            #neurons mems of next layer
            'output_ep': ['http://nod3:5000/send_nod_inputs',
                          'http://nod3:5000/send_nod_inputs'
                         ]
        }

        nod_2_neurons_input =  {
            'nod_id': '2',
            'capa_id': '2',
            'input_names': ['o1', 'o2'],
            'pesos': [
                [0.2804066, 0.4414947]
            ],
            'biases': [0.0],
            'fas': ['relu'],
            'output_names': ['o3'],
            'output_ep': ['http://localhost:5000/prediction_output'
                         ]
        }


        expected_result = {'result': 'neurons installed'}

        output = "[0, 1.2259113788604736]"

        headers = {'Content-type': 'application/json'}

        try:
            #Create a Synapses object which is meant to be the footprint
            #of a whole prediction process of an AI distributed model
            synapses_data = {
                "ai_model_path": "path of the model...",
                "distributed_model": "distributed model in json...",
                "other_needed_info": "to perform AI traceability"
            }
            json_data = json.dumps(synapses_data)
            #To the neuro orchestrator
            res = requests.post("http://localhost:7000/start_synapses_process",
                                data=json_data, headers=headers
                               )
            synapses_obj_mem_adr = json.loads(res.text)['syn_proc_id']

            #to the NOD 1
            json_data = json.dumps(nod_1_neurons_input)
            res = requests.post("http://localhost:5000/save_neurons",
                                   data=json_data, headers=headers
                                  )
            nodo_mem_adr_1 = json.loads(res.text)['nodo_mem_adr']

            #to the NOD 2
            json_data = json.dumps(nod_2_neurons_input)
            res = requests.post("http://localhost:6000/save_neurons",
                                   data=json_data, headers=headers
                                  )

            nodo_mem_adr_2 = json.loads(res.text)['nodo_mem_adr']


            #Send inputs to the first NOD. 2nd one should recieve from
            #the 1rst one proper inputs

            nod_input_1 = {
                "input_names": ["x1", "x2", "x3", "x4"],
                "inputs": [4, 5],
                "input_idx": [2, 3],
                "nodo_mem_adr": nodo_mem_adr_1,
                "nodo_mem_adr_dstn": [nodo_mem_adr_2] #should be a list
            }

            nod_input_2 = {
                "input_names": ["x1", "x2", "x3", "x4"],
                "inputs": [2, 3],
                "input_idx": [0, 1],
                "nodo_mem_adr": nodo_mem_adr,
                "nodo_mem_adr_dstn": [synapses_obj_mem_adr] #to neuro orchestrator
            }

            synapses_info = {
                "nodo_mem_adr": synapses_obj_mem_adr
            }

            # send_nod_inputs instead of set_nod_inputs, new EP to support mem
            # address for destination nods
            json_data = json.dumps(nod_input_1)
            result = requests.post("http://localhost:5000/send_nod_inputs",
                                   data=json_data, headers=headers
                                  ).text
            json_data = json.dumps(nod_input_2)
            result = requests.post("http://localhost:5000/send_nod_inputs",
                                   data=json_data, headers=headers
                                  ).text

            #Finally get the prediction
            json_data = json.dumps(synapses_info)
            result = requests.post("http://localhost:5000/get_synapses_prediction",
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

