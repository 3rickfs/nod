import json
from flask import Flask, request

app = Flask(__name__)

def save_nod_info_in_dict(nod_id, capa_id, input_names, pesos, biases, fas,
                          output_names, output_ep
                         ):
    jsn = {}
    jsn["nod_id"] = nod_id
    jsn["capa_id"] = capa_id
    jsn["input_names"] = input_names
    jsn["pesos"] = pesos
    jsn["biases"] = biases
    jsn["fas"] = fas
    jsn["output_names"] = output_names
    jsn["output_ep"] = output_ep

    return jsn

@app.route("/model_to_neuron_sets", methods = ['POST'])
def model_to_neuron_sets():
    json_data = request.get_json()

    info_layer = []
    # get layers info:
    for l in range(len(json_data["layers"])):
        layer_dict = json_data["layers"]["layer_" + str(l)]
        ws, bs, fas, ins, ons = [], [], [], []
        for n in range(len(layer_dict)):
            neuron_dict = layer_dict["neuron_" + str(n)]
            ws.append(neuron_dict["weights"]["w"])
            bs.append(neuron_dict["bias"])
            fas.append(neuron_dict["fs"])
            ins.append(neuron_dict["input_names"])
            ons.append(neuron_dict["output_names"])

        info_layer.append([ins, ws, bs, fas, ons])

    #split model:
    neurons_per_nod = json_data["neurons_per_nod"]
    nod_num = json_data["nod_num"]
    nod_ep = ["http://localhost:5000/final_prediction", #TODO: add this to list of endpoints
              ("a545ed66e46bc4ea788f4aada7bcea72-1944961211.",
              "us-west-1.elb.amazonaws.com:5000/exec_neurons"),
              ("a6823b10e5c7a4dd5a038a6f813091b4-242539242.",
              "us-west-1.elb.amazonaws.com:5000/exec_neurons")]

    nod_dict = {}
    #last layer just one neuron
    layers_num = len(json_data["layers"])
    neuron_num = len(info_layer[layer][2])
    nods_num = int(neuron_num / neurons_per_nod)
    nc = 1
    for layer in range(layers_num):
        if layer == layers_num - 1: #last layer
            nod_dict["nod_" + nc] = save_nod_info_in_dict(
                nc,
                layer + 1,
                info_layer[layer][0],
                info_layer[layer][1],
                info_layer[layer][2],
                info_layer[layer][3],
                info_layer[layer][4],
                nod_ep[0]
            )


        else:
            for nod in nods_num:
                for 

        nod_dict[



    return json_data['model_info']

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')

    app.run(host=host, port=int(port))
