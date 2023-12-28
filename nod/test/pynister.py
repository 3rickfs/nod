import json
from flask import Flask, request

app = Flask(__name__)

def not_repeat(input_names):
    #neurons mostly have same input names, removing repeatitions  
    #not sure is there is any reason to have different input names.
    #For now just considering one single array for same inputs
    return input_names[0]

def save_nod_info_in_dict(nod_id, capa_id, input_names, pesos, biases, fas,
                          output_names, output_ep
                         ):
    jsn = {}
    jsn["nod_id"] = str(nod_id)
    jsn["capa_id"] = str(capa_id)
    jsn["input_names"] = not_repeat(input_names)
    jsn["pesos"] = pesos
    jsn["biases"] = biases
    jsn["fas"] = fas
    #jsn["output_names"] = [
    #    [i,j] for i, j in zip(output_names[0][:], output_names[1][:])
    #][0] # making it just one array.
    jsn["output_names"] = output_names
    jsn["output_ep"] = [output_ep[0] for i in range(len(output_names))]

    return jsn

def get_nods_number(neuron_num, neurons_per_nod):
    div = neuron_num % neurons_per_nod
    if div == 0:
        nods_num = int(neuron_num / neurons_per_nod)
    else:
        nods_num = int(neuron_num / neurons_per_nod) + 1

    return nods_num

def read_endpoints(fpath):
    #reading endpoints
    eps = []
    with open("./nod_endpoints.txt", "r") as ep_file:
        eps = [line.rstrip() for line in ep_file]
        #while True:
        #    ep = ep_file.readline()
        #    if not ep:
        #        break
        #    else:
        #        eps.append(ep)
        ep_file.close()
    return eps

@app.route("/model_to_neuron_sets", methods = ['POST'])
def model_to_neuron_sets():
    json_data = request.get_json()
    #split parameters model:
    neurons_per_nod = json_data["CoN_parameters"]["neurons_per_nod"]
    nod_num = json_data["CoN_parameters"]["nod_num"]
    #this will be used for the neuro orchestrator to send json to nods too
    nod_ep = read_endpoints("./nod_endpoints.txt")
    neuro_orchestrator_ep = ["http://localhost:5000/final_prediction"]
    info_layer = []
    # get layers info:
    nc = 1 #neurons counter
    noc = 0 #nod counter
    for l in range(1, len(json_data["layers"])+1):
        layer_dict = json_data["layers"]["layer_" + str(l)]

        neuron_num = len(layer_dict)
        nods_num = get_nods_number(neuron_num, neurons_per_nod) 

        ws, bs, fas, ins, ons, eps = [], [], [], [], [], []
        for n in range(1, neuron_num+1):
            neuron_dict = layer_dict["neuron_" + str(nc)]
            ws.append(neuron_dict["pesos"]["w"])
            bs.append(neuron_dict["bias"])
            fas.append(neuron_dict["fa"])
            ins.append(neuron_dict["inputs_names"])
            ons.append(neuron_dict["outputs_names"][0])
            nc += 1
        #list of NOD endpoints in current layer
        eps = nod_ep[noc:noc+nods_num]
        noc += nods_num

        info_layer.append([ins, ws, bs, fas, ons, eps])

    nod_dict = {}
    #last layer just one neuron
    layers_num = len(info_layer)
    noc = 1
    for layer in range(layers_num):
        if layer == layers_num - 1: #last layer
            nod_dict["nod_" + str(noc)] = save_nod_info_in_dict(
                noc,
                layer + 1,
                info_layer[layer][0],
                info_layer[layer][1],
                info_layer[layer][2],
                info_layer[layer][3],
                info_layer[layer][4],
                neuro_orchestrator_ep #to the pynister
            )
            noc = 1
        else:
            #for j in range(0, len(info_layer[layer][2]), #nods_num):
            neuron_num = len(info_layer[layer][2])
            nods_num = len(info_layer[layer][5]) #int(neuron_num / neurons_per_nod)
            for j in range(0, neuron_num, neurons_per_nod):
                nod_dict["nod_" + str(noc)] = save_nod_info_in_dict(
                    noc,
                    layer + 1,
                    info_layer[layer][0],
                    info_layer[layer][1][j:j+neurons_per_nod], #neuron_num],
                    info_layer[layer][2][j:j+neurons_per_nod],  #neuron_num],
                    info_layer[layer][3][j:j+neurons_per_nod], #neuron_num],
                    info_layer[layer][4],
                    info_layer[layer+1][5] #ep to the next neuron in next layer
                )
                nods_num -= 1 #every time it's added a new nod
            noc += 1
            if nods_num > 0:
                #it left one nod to be added, there're more neurons yet
                nod_dict["nod" + str(noc)] = save_nod_info_in_dict(
                    noc,
                    layer + 1,
                    info_layer[layer][0],
                    info_layer[layer][1][j:],
                    info_layer[layer][2][j:],
                    info_layer[layer][3][j:],
                    info_layer[layer][4],
                    info_layer[layer+1][5] #ep to the next neuron in next layer
                )

    return json.dumps(nod_dict) #json_data['model_info']

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')

    app.run(host=host, port=int(port))
