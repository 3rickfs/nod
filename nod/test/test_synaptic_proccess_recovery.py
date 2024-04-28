import unittest
import requests

no_url = "http://127.0.0.1:5000"

class sp_nod_info_recovery_tests(unittest.TestCase):

    def test_sp_recovery(self):
        print("*"*100)
        print("Test 1: when nod service starts it should load the saved sp")
        print("-------------------------------------------------------------")

        try:
            data = {}
            data["synapses_process_id"] = 16
            data["detailed_res"] = False

            json_data = json.dumps(data)

            headers = {'Content-type': 'application/json'}
            ep = no_url + "/get_sp_nod_info"
            result = requests.post(ep,
                                   data=json_data,
                                   headers=headers
                                  )
            expected_result = 2
            result = json.loads(result.text)["nod_id"]

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

