import requests
import json

def start_distribution(nod_dict, nod_ep):
    """ Start distributing neurons to every NOD according
        to the previuosly stablished plan.
    """

    nod_res = []
    for nod_idx in range(1, len(nod_dict) + 1):
        nod_d = nod_dict["nod_" + str(nod_idx)]
        json_data = json.dump(nod_d)
        headers = {'Content-type': 'application/json'}
        #TODO: save obj mem addrs info of every nod to be saved in the
        # synpase process obj
        print(f"Sending to: {nod_ep[nod_idx-1]}")
        result = requests.post(nod_ep[nod_idx-1],
                               data=json_data,
                               headers=headers
                              )
        print(f"result: {result.text}")
        nod_res.append(result.text)

    return nod_res


