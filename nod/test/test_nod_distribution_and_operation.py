import unittest
import time
import requests
import json

import keras
import numpy as np

class distribution_tests(unittest.TestCase):

    def test_execute_distributed_model_locally_1(self):
        print("*"*100)
        print("Test 1: distirbute neurons to two NODs for a small dense layer"\
              " based model distribution and run it locally")
        print("-------------------------------------------------------------")

        input_file_name = "model_to_be_distributed_and_executed_1.json"
        CoN_parameters = {
            "neurons_per_nod": 2,
            "nod_num": 10
        }

        #Run above model in TF format to get the expected result
        model = keras.models.load_model(
            "./model_to_be_distributed_and_executed_1.keras"
        )
        inp_dic = [2, 3, 4, 5]
        inp = np.array(inp_dic).reshape(1, 4)
        print(f"model input: {inp}")
        expected_result = str(round(model.predict(inp)[0][0], 4)) #[1.5349037952800018]
        print(expected_result)

        try:

            #Starting synapses process
            headers = {'Content-type': 'application/json'}
            syn_pro_input = {
                "ai_model_path": "lala.model",
                "distributed_model": "whole distributed model"
            }

            json_data = json.dumps(syn_pro_input)
            result = requests.post("http://localhost:7000/start_synapses_process",
                                   data=json_data, headers=headers
                                  )

            synapses_process_id = json.loads(result.text)["synapses_process_id"]

            #Load the AI model JSON
            with open(input_file_name, 'r') as jf:
                input_json_file = json.load(jf)
            jf.close()

            #Distribute neurons
            input_json_file["CoN_parameters"] = CoN_parameters
            input_json_file["nod_ops_endpoints"] = "./nod_ops_endpoints.txt"
            input_json_file["nod_dis_endpoints"] = "./nod_dis_endpoints.txt"
            input_json_file["synapses_process_id"] = synapses_process_id
            json_data = json.dumps(input_json_file)
            result = requests.post("http://localhost:7000/distribute_neurons",
                                   data=json_data, headers=headers
                                  )

            #send inputs to NODS
            nod_input = {
                "input_names": ["x1", "x2", "x3", "x4"],
                "inputs": inp_dic,
                "input_idx": [0, 1, 2, 3], #double check this
                "synapses_process_id": synapses_process_id
            }

            json_data = json.dumps(nod_input)
            result = requests.post("http://localhost:7000/send_inputs_to_1layer_nods",
                                   data=json_data, headers=headers
                                  )

            #It will take some time to process and update corresponding objects
            #for now I just will wait a little bit
            time.sleep(2)
            info = {
                "synapses_process_id": synapses_process_id
            }

            #Read the output after running the model
            json_data = json.dumps(info)
            result = requests.post("http://localhost:7000/read_synapses_process_output",
                                   data=json_data, headers=headers
                                  )
            result = str(round(json.loads(result.text)[0], 4))

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

    def test_execute_distributed_model_locally_2(self):
        print("*"*100)
        print("Test 2: distirbute neurons to six NODs for a larger dense layer"\
              " based model distribution and run it locally")
        print("-------------------------------------------------------------")

        input_file_name = "model_to_be_distributed_and_executed_2.json"
        CoN_parameters = {
            "neurons_per_nod": 4,
            "nod_num": 10
        }

        #Run above model in TF format to get the expected result
        model = keras.models.load_model(
            "./model_to_be_distributed_and_executed_2.keras"
        )
        inp_dic = [2, 3, 4, 5, 8]
        inp = np.array(inp_dic).reshape(1, 5)
        print(f"model input: {inp}")
        pred = model.predict(inp)
        print(f"pred: {pred}")
        expected_result = str(round(pred[0][0], 4)) #[1.5349037952800018]
        print(expected_result)

        try:

            #Starting synapses process
            headers = {'Content-type': 'application/json'}
            syn_pro_input = {
                "ai_model_path": "lala.model",
                "distributed_model": "whole distributed model"
            }

            json_data = json.dumps(syn_pro_input)
            result = requests.post("http://localhost:7000/start_synapses_process",
                                   data=json_data, headers=headers
                                  )

            synapses_process_id = json.loads(result.text)["synapses_process_id"]

            #Load the AI model JSON
            with open(input_file_name, 'r') as jf:
                input_json_file = json.load(jf)
            jf.close()

            #Distribute neurons
            input_json_file["CoN_parameters"] = CoN_parameters
            input_json_file["nod_ops_endpoints"] = "./nod_ops_endpoints.txt"
            input_json_file["nod_dis_endpoints"] = "./nod_dis_endpoints.txt"
            input_json_file["synapses_process_id"] = synapses_process_id
            json_data = json.dumps(input_json_file)
            result = requests.post("http://localhost:7000/distribute_neurons",
                                   data=json_data, headers=headers
                                  )

            #send inputs to NODS
            nod_input = {
                "input_names": ["x1", "x2", "x3", "x4", "x5"],
                "inputs": inp_dic,
                "input_idx": [0, 1, 2, 3, 4], #double check this
                "synapses_process_id": synapses_process_id
            }

            json_data = json.dumps(nod_input)
            result = requests.post("http://localhost:7000/send_inputs_to_1layer_nods",
                                   data=json_data, headers=headers
                                  )

            #It will take some time to process and update corresponding objects
            #for now I just will wait a little bit
            time.sleep(2)
            info = {
                "synapses_process_id": synapses_process_id
            }

            #Read the output after running the model
            json_data = json.dumps(info)
            result = requests.post("http://localhost:7000/read_synapses_process_output",
                                   data=json_data, headers=headers
                                  )
            #print(f"result: {result.text}")
            result = str(round(json.loads(result.text)[0], 4))

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

    def test_execute_distributed_model_locally_3(self):
        print("*"*100)
        print("Test 3: distirbute neurons to six NODs for a deep dense layer"\
              " based model distribution and run it locally: diabetes model")
        print("-------------------------------------------------------------")

        input_file_name = "diabetes_detection_model.json"
        CoN_parameters = {
            "neurons_per_nod": 80,
            "nod_num": 10
        }

        #Run above model in TF format to get the expected result
        model = keras.models.load_model(
            "./diabetes_detection_model.keras"
        )
        inp_dic = [1,0,1,1,0,1,0,0,0,1,0,1,1,0,0,1,
                   1,0,0,1,1,0,0,0,1,1,1,1,1,0,0
                  ]
        inp = np.array(inp_dic).reshape(1, 31)
        print(f"model input: {inp}")
        pred = model.predict(inp)
        print(f"pred: {pred}")
        #expected_result = str(pred) #[1.5349037952800018]
        expected_result = [str(round(v, 4)) for v in pred[0]]
        print(expected_result)

        try:

            #Starting synapses process
            headers = {'Content-type': 'application/json'}
            syn_pro_input = {
                "ai_model_path": "lala.model",
                "distributed_model": "whole distributed model"
            }

            json_data = json.dumps(syn_pro_input)
            result = requests.post("http://localhost:7000/start_synapses_process",
                                   data=json_data, headers=headers
                                  )

            synapses_process_id = json.loads(result.text)["synapses_process_id"]

            #Load the AI model JSON
            with open(input_file_name, 'r') as jf:
                input_json_file = json.load(jf)
            jf.close()

            #Distribute neurons
            input_json_file["CoN_parameters"] = CoN_parameters
            input_json_file["nod_ops_endpoints"] = "./nod_ops_endpoints.txt"
            input_json_file["nod_dis_endpoints"] = "./nod_dis_endpoints.txt"
            input_json_file["synapses_process_id"] = synapses_process_id
            json_data = json.dumps(input_json_file)
            result = requests.post("http://localhost:7000/distribute_neurons",
                                   data=json_data, headers=headers
                                  )

            #send inputs to NODS
            nod_input = {
                "input_names": ["x1", "x2", "x3", "x4", "x5", "x6",
                                "x7", "x8", "x9", "x10", "x11", "x12",
                                "x13", "x14", "x15", "x16", "x17", "x18",
                                "x19", "x20", "x21", "x22", "x23", "x24",
                                "x25", "x26", "x27", "x28", "x29", "x30", "x31",
                               ],
                "inputs": inp_dic,
                "input_idx": [i for i in range(31)],
                "synapses_process_id": synapses_process_id
            }

            json_data = json.dumps(nod_input)
            result = requests.post("http://localhost:7000/send_inputs_to_1layer_nods",
                                   data=json_data, headers=headers
                                  )

            #It will take some time to process and update corresponding objects
            #for now I just will wait a little bit
            time.sleep(2)
            info = {
                "synapses_process_id": synapses_process_id
            }

            #Read the output after running the model
            json_data = json.dumps(info)
            result = requests.post("http://localhost:7000/read_synapses_process_output",
                                   data=json_data, headers=headers
                                  )
            #print(f"result: {result.text}")
            r = json.loads(result.text)
            result = [str(round(v, 4)) for v in r]

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


if __name__ == '__main__':
    unittest.main()

