import requests
import json

def start_distribution(nod_dict, nod_eps, synapses_process_id):
    """ Start distributing neurons to every NOD according
        to the previuosly stablished plan.
    """

    nod_res = []
    for nod_idx in range(1, len(nod_dict) + 1):
        nod_d = nod_dict["nod_" + str(nod_idx)]
        nod_d["synapses_process_id"] = synapses_process_id
        json_data = json.dumps(str(nod_d))
        headers = {'Content-type': 'application/json'}
        #TODO: save obj mem addrs info of every nod to be saved in the
        # synpase process obj
        print(f"Sending to: {nod_eps[nod_idx-1]}")
        result = requests.post(nod_eps[nod_idx-1],
                               data=json_data,
                               headers=headers
                              )
        print(f"result: {result.text}")
        nod_res.append(result.text)

    return nod_res

def start_first_layer_input_distribution(nod_input, nod_eps):
    """ Distribute same input to every single nod in first layer
    """

    json_data = json.dumps(nod_input)
    nod_res = []
    headers = {'Content-type': 'application/json'}
    for nod_ep in nod_eps:
        print(f"Sending inputs to nod: {nod_ep}")
        result = requests.post(nod_ep,
                               data=json_data,
                               headers=headers
                              )
        nod_res.append(result.text)

    return nod_res
