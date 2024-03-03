import unittest
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


if __name__ == '__main__':
    unittest.main()
