import unittest
import requests
import json

from nod.nod import nod

class neuron_ops_test_cases(unittest.TestCase):
    def test_api_hello_world(self):
        print("*"*100)
        print("Test 1: call http://IP:PORT/ to get hello world greetings from"\
              "a node running in an EKS cluster!")
        print("-------------------------------------------------------------")
        expected_result = ("<p>Hello, World! I'm a virtual NOD (Neuro Orches"
                           "trated Device) running in EKS cluster in AWS as a"
                           " pod. So I'm ready for running multiple neurons."
                           " Nice to meet you.</p>")

        try:
            result = requests.get(("http://a545ed66e46bc4ea788f4aada7bcea72-"
                                   "1944961211.us-west-1.elb.amazonaws.com:5000/"))
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

    def test_model_json_to_neuron_set_jsons(self):
        print("*"*100)
        print("Test 2: call http://IP:PORT/model_to_neuron_sets to split the"
               "whole model in json into group of neurons in json too.")
        print("-------------------------------------------------------------")
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
                "pesos": [[-0.4397721290588379, -0.8503506183624268, 0.11941719055175781, 0.28388309478759766],
                          [-0.8684360980987549, -0.2745087146759033, 0.3909769058227539, 0.44448041915893555]
                         ],
                "biases": [0.0, 0.0],
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
                "pesos": [[0.9150172472000122, -0.647889256477356],
                          [-0.6167148351669312, 1.1931308507919312]
                         ],
                "biases": [0.0, 0.0],
                "fas": ['relu', 'relu'],
                "output_names": ['o3', 'o4'],
                "output_ep":["http://localhost:5000/final_prediction",
                             "http://localhost:5000/final_prediction"
                            ]
            }
        }

        try:
            with open(input_file_name, 'rb') as jf:
                input_json_file = json.load(jf)
            #print(f"json file: {input_json_file}")
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
            self.assertEqual(expected_result, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)


    def test_model_json_to_neuron_set_jsons_2(self):
        print("*"*100)
        print("Test 3: again call http://IP:PORT/model_to_neuron_sets to split the"
               "whole model (another one) in json into group of neurons in json too.")
        print("-------------------------------------------------------------")
        input_file_name = "./test_dense_model_2.json"
        CoN_parameters = {
            "neurons_per_nod": 2,
            "nod_num": 10
        }
        expected_result = {
            "nod_1": {
                "nod_id": "1",
                "capa_id": "1",
                "input_names": ['x1', 'x2', 'x3', 'x4', 'x5'],
                "pesos": [
                    [0.171137273311615, 0.17062145471572876, -0.23058700561523438, -0.2599382996559143, 0.12979340553283691],
                    [0.02977389097213745, 0.2760855555534363, -0.6309725046157837, 0.581677258014679, -0.47849205136299133]
                ],
                "biases": [0.0, 0.0],
                "fas": ['relu', 'relu'],
                "output_names": ['o1', 'o2'],
                "output_ep":["http://nod3:5000/exec_neurons",
                             "http://nod3:5000/exec_neurons"]
            },
            "nod_2": {
                "nod_id": "2",
                "capa_id": "1",
                "input_names": ['x1', 'x2', 'x3', 'x4', 'x5'],
                "pesos": [
                    [0.17120105028152466, 0.2488141655921936, -0.2648974061012268, 0.2123282551765442, -0.485383003950119]
                ],
                "biases": [0.0],
                "fas": ['relu'],
                "output_names": ['o3'],
                "output_ep":["http://nod3:5000/exec_neurons"]
            },
            "nod_3": {
                "nod_id": "3",
                "capa_id": "2",
                "input_names": ['o1', 'o2', 'o3'],
                "pesos": [
                    [0.0460209846496582, 0.21512341499328613, 0.16031408309936523]
                ],
                "biases": [0.0],
                "fas": ['relu'],
                "output_names": ['o4'],
                "output_ep":["http://localhost:5000/final_prediction"]
            }
        }

        try:
            with open(input_file_name, 'rb') as jf:
                input_json_file = json.load(jf)
            #print(f"json file: {input_json_file}")
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
            self.assertEqual(expected_result, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

    def test_model_json_to_neuron_set_jsons_3(self):
        print("*"*100)
        print("Test 4: again call http://IP:PORT/model_to_neuron_sets to split the"
               "whole model (another bigger one) in json into group of neurons in json too.")
        print("-------------------------------------------------------------")
        input_file_name = "./test_dense_model_3.json"
        CoN_parameters = {
            "neurons_per_nod": 2,
            "nod_num": 10
        }
        expected_result = {
            "nod_1": {
                "nod_id": "1",
                "capa_id": "1",
                "input_names": ['x1', 'x2', 'x3', 'x4', 'x5'],
                "pesos": [
                    [-0.5181081891059875, -0.4963250458240509, 0.4666529893875122, 0.37765979766845703, 0.40111005306243896],
                    [0.1149454116821289, 0.023162007331848145, -0.48261186480522156, -0.1083630919456482, 0.16650164127349854]
                ],
                "biases": [0.0, 0.0],
                "fas": ['relu', 'relu'],
                "output_names": ['o1', 'o2'],
                "output_ep":["http://nod3:5000/exec_neurons",
                             "http://nod3:5000/exec_neurons"]
            },
            "nod_2": {
                "nod_id": "2",
                "capa_id": "1",
                "input_names": ['x1', 'x2', 'x3', 'x4', 'x5'],
                "pesos": [
                    [-0.49771204590797424, -0.5319453477859497, -0.6112353801727295, -0.5461881160736084, -0.6803240180015564],
                    [-0.18595075607299805, -0.06585848331451416, 0.3084690570831299, -0.3852391242980957, 0.280637264251709]
                ],
                "biases": [0.0, 0.0],
                "fas": ['relu', 'relu'],
                "output_names": ['o3', 'o4'],
                "output_ep":["http://nod3:5000/exec_neurons",
                             "http://nod3:5000/exec_neurons"]
            },
            "nod_3": {
                "nod_id": "3",
                "capa_id": "2",
                "input_names": ['o1', 'o2', 'o3', 'o4'],
                "pesos": [
                    [-0.3568456172943115, 0.3078184127807617, 0.975879430770874, -0.07994365692138672],
                    [0.10254168510437012, 0.6220033168792725, 0.3412501811981201, 0.7440774440765381]
                ],
                "biases": [0.0, 0.0],
                "fas": ['relu', 'relu'],
                "output_names": ['o5', 'o6'],
                "output_ep":["http://nod4:5000/exec_neurons",
                             "http://nod4:5000/exec_neurons"]
            },
            "nod_4": {
                "nod_id": "4",
                "capa_id": "3",
                "input_names": ['o5', 'o6'],
                "pesos": [
                    [-1.4004716873168945, -0.9295446872711182]
                ],
                "biases": [0.0],
                "fas": ['relu'],
                "output_names": ['o7'],
                "output_ep":["http://localhost:5000/final_prediction"]
            }

        }

        try:
            with open(input_file_name, 'rb') as jf:
                input_json_file = json.load(jf)
            #print(f"json file: {input_json_file}")
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
            self.assertEqual(expected_result, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

    def test_model_json_to_neuron_set_jsons_4(self):
        print("*"*100)
        print("Test 5: again call http://IP:PORT/model_to_neuron_sets to split the"
               "whole model (another bigger one) in json into group of neurons in json too.")
        print("-------------------------------------------------------------")
        input_file_name = "./test_dense_model_4.json"
        CoN_parameters = {
            "neurons_per_nod": 2,
            "nod_num": 10
        }
        expected_result = {} #just to see the result variable by now

        try:
            with open(input_file_name, 'rb') as jf:
                input_json_file = json.load(jf)
            #print(f"json file: {input_json_file}")
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
            self.assertEqual(expected_result, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

    def test_model_json_to_neuron_set_jsons_5(self):
        print("*"*100)
        print("Test 6: call  http://IP:PORT/model_to_neuron_sets to split the"
               "whole model in json into group of three neurons/nod.")
        print("-------------------------------------------------------------")
        input_file_name = "./test_dense_model_4.json"
        CoN_parameters = {
            "neurons_per_nod": 3,
            "nod_num": 30
        }
        expected_result = {} #just to see the result variable by now

        try:
            with open(input_file_name, 'rb') as jf:
                input_json_file = json.load(jf)
            #print(f"json file: {input_json_file}")
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
            self.assertEqual(expected_result, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

"""

    def test_model_json_to_neuron_set_jsons_6(self):
        print("*"*100)
        print("Test 7: testing first deep neural network")
        print("-------------------------------------------------------------")
        input_file_name = "./diabetes_detection_model.json"
        CoN_parameters = {
            "neurons_per_nod": 50,
            "nod_num": 30
        }
        expected_result = {} #just to see the result variable by now

        try:
            with open(input_file_name, 'rb') as jf:
                input_json_file = json.load(jf)
            #print(f"json file: {input_json_file}")
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
            self.assertEqual(expected_result, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

"""

if __name__ == '__main__':
    unittest.main()

