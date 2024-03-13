import unittest
import time
import keras
import numpy as np
from nod.nod import nod

class neuron_ops_test_cases(unittest.TestCase):
    def test_input_homogeneo_asincrono(self):
        print("*"*100)
        print("Test 1: test homogeneous and asyncronous input for a " \
              "two-layer based neuron structure")

        expected_result = {'input_names': ['o0', 'o1', 'o2', 'o3'],
                           'inputs': [20, 21, 22, 23]}
        nod_data = {
            "nod_id": "0",
            "pesos": [[[1,2,3], [1,2,3], [1,2,3]], [[1,2,3], [1,2,3]]],
            "biases": [[1, 1, 1], [0, 0]],
            "fas": [["relu", "relu", "relu"], ["relu", "relu"]],
            "capa_ids": [0, 1],
            "output_names": [["o0", "o1", "o2"], ["o3", "o4"]],
            "output_port": ["6339"], #this is no longer needed
            "input_names": [["i0", "i1", "i2"], ["o0", "o1", "o2"]],
            "output_eps": ["192.168.0.1:5000"],
            "input_num": [3, 3],
            "inputs": [[0, 0, 0], [0, 0, 0]], # no needed
            "neuron_outputs": [0, 0], # no needed
            "synapses_process_id": 123
        }

        test_nod = nod()
        test_nod.read_parameters(nod_data)

        input_msg_1 = { # or output_msg from previous layer
                        "input_names": ["i0", "i1"],
                        "inputs": [2, 3],
                        "input_idx": [0, 1],
                        "layer_id": 1
                      }
        input_msg_2 = { # or output_msg from previous layer
                        "input_names": ["i2"],
                        "inputs": [3],
                        "input_idx": [2],
                        "layer_id": 1
                      }

        #Primer entrada de input
        if test_nod.set_inputs(input_msg_1["inputs"],
                                input_msg_1["input_names"],
                                input_msg_1["input_idx"],
                                input_msg_1["layer_id"]
                               ) and \
           test_nod.set_inputs(input_msg_2["inputs"],
                                input_msg_2["input_names"],
                                input_msg_2["input_idx"],
                                input_msg_2["layer_id"]
                               ):
            try:
                result = test_nod.get_neuron_outputs() #test_nod.run_neuron_ops()
                print(f"expected_result: {expected_result}")
                print(f"output_msg: {result['output_msg']}")
                self.assertEqual(expected_result, result["output_msg"])
            except Exception as e:
                print("-"*100)
                print(f"error: {e}")
                print("-"*100)

        else:
            print("Error running neuron_ops,input rejected")
        print("*"*100)

    def test_input_homogeneo_asincrono(self):
        print("*"*100)
        print("Test 2: test homogeneous and asyncronous input for a " \
              "two-layer based neuron structure remote and local")

        model = keras.models.load_model(
            "./test_dense_model_5.keras"
        )
        inp_dic = [2,3,3]
        inp = np.array(inp_dic).reshape(1, 3)
        print(f"model input: {inp}")
        start = time.time()
        pred = model.predict(inp)
        end = time.time()
        print(f"pred: {pred}")
        print(f"Local prediction time: {end-start}")
        #expected_result = str(pred) #[1.5349037952800018]
        expected_result = [str(round(v, 4)) for v in pred[0]]
        print(expected_result)

        expected_result = {'input_names': ['o0', 'o1', 'o2', 'o3'],
                           'inputs': [20, 21, 22, 23]}
        nod_data = {
            "nod_id": "0",
            "pesos": [[
                [0.24543380737304688,-0.6091499328613281, 0.9680633544921875],
                [-0.41131043434143066,0.2982015609741211,-0.023629426956176758],
                [-0.9772284030914307,-0.7074456214904785,0.025614261627197266]],
                [[1.0473427772521973,0.7940226793289185,0.36034369468688965],
                 [0.9023321866989136,0.8934919834136963,0.9905946254730225]]],
            "biases": [[0, 0, 0], [0, 0]],
            "fas": [["relu", "relu", "relu"], ["relu", "relu"]],
            "capa_ids": [0, 1],
            "output_names": [["o0", "o1", "o2"], ["o3", "o4"]],
            "output_port": ["6339"],
            "input_names": [["i0", "i1", "i2"], ["o0", "o1", "o2"]],
            "output_eps": ["192.168.0.1:5000"],
            "input_num": [3, 3],
            "inputs": [[0, 0, 0], [0, 0, 0]],
            "neuron_outputs": [0, 0],
            "synapses_process_id": 123
        }

        test_nod = nod()
        test_nod.read_parameters(nod_data)

        input_msg_1 = { # or output_msg from previous layer
                        "input_names": ["i0", "i1"],
                        "inputs": [2, 3],
                        "input_idx": [0, 1],
                        "layer_id": 0
                      }
        input_msg_2 = { # or output_msg from previous layer
                        "input_names": ["i2"],
                        "inputs": [3],
                        "input_idx": [2],
                        "layer_id": 0
                      }

        #Primer entrada de input
        start = time.time()
        if test_nod.set_inputs(input_msg_1["inputs"],
                                input_msg_1["input_names"],
                                input_msg_1["input_idx"],
                                input_msg_1["layer_id"]
                               ) and \
           test_nod.set_inputs(input_msg_2["inputs"],
                                input_msg_2["input_names"],
                                input_msg_2["input_idx"],
                                input_msg_2["layer_id"]
                               ):
            try:
                result = test_nod.get_neuron_outputs() #test_nod.run_neuron_ops()
                end = time.time()
                print(f"distributed prediction time: {end-start}")
                print(f"expected_result: {expected_result}")
                print(f"output_msg: {result['output_msg']}")
                self.assertEqual(expected_result, result["output_msg"])
            except Exception as e:
                print("-"*100)
                print(f"error: {e}")
                print("-"*100)

        else:
            print("Error running neuron_ops,input rejected")
        print("*"*100)

if __name__ == '__main__':
    unittest.main()
