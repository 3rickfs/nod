import os
from abc import ABC, abstractmethod
import json

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
        ep_file.close()
    return eps

class orc_pla_ops(ABC):
    """ Orchestration planning operations
    """

    @abstractmethod
    def run_operation(**kwargs):
        #intergace to child clasess
        pass

class get_model_components(orc_pla_ops):
    """ Get model's weights, biases, activation funcitions, etc.
    """
    def run_operation(**kwargs):
        json_data = kwargs["json_data"]
        nod_ep = kwargs["nod_ep"]
        #split parameters model:
        neurons_per_nod = json_data["CoN_parameters"]["neurons_per_nod"]
        nod_num = json_data["CoN_parameters"]["nod_num"]
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

        kwargs["info_layer"] = info_layer

        return kwargs

class create_nod_dictionary(orc_pla_ops):
    """ NOD dictionary in which every NOD can read what it's needed to do
        according to the orchestration plan
    """

    def run_operation(**kwargs):
        info_layer = kwargs["info_layer"]
        nod_dict = {}
        neuro_orchestrator_ep = kwargs["neuro_orchestrator_ep"]
        neurons_per_nod = kwargs["json_data"]\
                                ["CoN_parameters"]\
                                ["neurons_per_nod"]
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
                neuron_num = len(info_layer[layer][2])
                for j in range(0, neuron_num, neurons_per_nod):
                    nod_dict["nod_" + str(noc)] = save_nod_info_in_dict(
                        noc,
                        layer + 1,
                        info_layer[layer][0],
                        info_layer[layer][1][j:j+neurons_per_nod],
                        info_layer[layer][2][j:j+neurons_per_nod],
                        info_layer[layer][3][j:j+neurons_per_nod],
                        info_layer[layer][4][j:j+neurons_per_nod],
                        #ep to the next neuron in next layer
                        info_layer[layer+1][5]
                    )
                    noc += 1

        kwargs["nod_dict"] = nod_dict

        return kwargs

class OrchPlannerOps:

    @staticmethod
    def run(**kwargs):
        for operation in orc_pla_ops.__subclasses__():
            kwargs = operation.run_operation(**kwargs)

        return kwargs

