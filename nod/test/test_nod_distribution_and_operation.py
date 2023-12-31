import unittest
import requests
import json

from nod.nod import nod

class distribution_tests(unittest.TestCase):
    def test_distribution_1(self):
        print("*"*100)
        print("Test 1: distirbute neurons to two NODs for a small dense layer"\
              " based model distribution") 
        print("-------------------------------------------------------------")

        expected_result_nod_1 = {
            "result": "neurons installed"
        }
        expected_result_nod_2 = {
            "result": "neurons installed"
        }

        try:
            with open(input_file_name, 'rb') as jf:
                input_json_file = json.load(jf)
            #adding parameters of Cluster of Neurons
            input_json_file["CoN_parameters"] = CoN_parameters
            json_data = json.dumps(input_json_file)
            headers = {'Content-type': 'application/json'}
            result = requests.post("http://localhost:5000/distribute_neurons",
                                   data=json_data, headers=headers
                                  )


            print("__________________________________")
            print(f"result: {result.text}")
            print("__________________________________")
            print(f"expected_result: {expected_result}")
            self.assertEqual(expected_result_nod_1, json.loads(result.text))
            self.assertEqual(expected_result_nod_2, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)

    def test_execute_distributed_model_locally_1(self):
        print("*"*100)
        print("Test 2: distirbute neurons to two NODs for a small dense layer"\
              " based model distribution and run it locally")
        print("-------------------------------------------------------------")



        input_file_name = "model_to_be_distributed_and_executed_1.json"
        CoN_parameters = {
            "neurons_per_nod": 2,
            "nod_num": 10
        }

        try:

            with open(input_file_name, 'rb') as jf:
                    input_json_file = json.load(jf)
            input_json_file["CoN_parameters"] = CoN_parameters
            input_json_file["nod_ops_endpoints"] = "./nod_ops_endpoints.txt"
            input_json_file["nod_dis_endpoints"= "./nod_dis_endpoints.txt"
            json_data = json.dumps(input_json_file)
            headers = {'Content-type': 'application/json'}
            result = requests.post("http://localhost:7000/distribute_neurons",
                                   data=json_data, headers=headers
                                  )





            print("__________________________________")
            print(f"result: {result.text}")
            print("__________________________________")
            print(f"expected_result: {expected_result}")
            self.assertEqual(expected_result_nod_1, json.loads(result.text))
        except Exception as e:
            print("%"*100)
            print(f"error: {e}")
            print("%"*100)

        print("*"*100)



if __name__ == '__main__':
    unittest.main()

