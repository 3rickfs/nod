import requests

def start_distributon(nod_dict, nod_ep):
    """ Start distributing neurons to every NOD according
        to the previuosly stablished plan.
    """

    nod_res = []
    for nod_idx in range(1, len(nod_dict) + 1):
        nod_d = nod_dict["nod_" + nod_idx]
        json_data = json.dumps(nod_d)
        headers = {'Content-type': 'application/json'}
        result = requests.post(nod_ep[nod_idx-1],
                               data=json_data,
                               headers=headers
                              )
        nod_res.append(result)

    return nod_res


