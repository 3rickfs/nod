import json
import requests
import ctypes
from flask import Flask, request

from orchestration_planner import read_endpoints, OrchPlannerOps
from synapses import synapses_process
from neuron_distributor import start_distribution,
                               start_first_layer_input_distribution

app = Flask(__name__)
syn_proc = None

def get_synapses_obj_memory_address(synapses_process_id):
    print("Getting synapses object memory address")
    with open("synapses_processes.json", "r") as jsonfile:
        synapses_processes = json.load(jsonfile)
    jsonfile.close()

    return synapses_processes[str(synapses_process_id)]

def get_fleps(nod_info):
    print("Getting first layer endpoints")
    fleps = []
    for nodi in nod_info:
        if nod_info[nodi]["capa_id"] == 1: #first layer
            fleps.append(nod_info[nodi]["output_ep"])
        else:
            break

    return fleps

@app.route("/model_to_neuron_sets", methods = ['POST'])
def model_to_neuron_sets():
    nod_dict = {}
    #this will be used for the neuro orchestrator to send json to nods too
    nod_ep = read_endpoints("./nod_endpoints.txt")
    neuro_orchestrator_ep = ["http://localhost:5000/final_prediction"]
    json_data = request.get_json()
    try:
        nod_dict = OrchPlannerOps.run(
            nod_ep = nod_ep,
            neuro_orchestrator_ep = neuro_orchestrator_ep,
            json_data = json_data
        )["nod_dict"]
    except Exception as e:
        print(f"error during orchestration planning: {e}")

    return json.dumps(nod_dict) #json_data['model_info']

@app.route("/distribute_neurons", methods = ['POST'])
def distribute_neurons():
    nod_dict = {}
    json_data = request.get_json()
    synapses_process_id = json_data["synapses_process_id"]
    #to save info about first layer endpoint to be used later
    syn_proc = ctypes.cast(
        int(synapses_process_id),
        ctypes.py_object
    ).value
    #this will be used for the neuro orchestrator to send json to nods too
    #nod_ep = read_endpoints("./nod_endpoints.txt")
    #this EP are to share ops info btw NODs
    nod_ops_ep = read_endpoints(json_data["nod_ops_endpoints"])
    #Need other EP to send neuorns info from NO to NODs
    nod_dis_ep = read_endpoints(json_data["nod_dis_endpoints"])

    #TODO: this neuro_orchestrator should be dynamically assigned
    neuro_orchestrator_ep = ["http://localhost:7000/set_final_output"]

    #Orchestration planning
    try:
        nod_dict = OrchPlannerOps.run(
            nod_ep = nod_ops_ep,
            neuro_orchestrator_ep = neuro_orchestrator_ep,
            json_data = json_data
        )["nod_dict"]
    except Exception as e:
        print(f"error during orchestration planning: {e}")
    #TODO: add new variable first_layer_eps to handle eps to be used later
    #Getting first layer endpoints and save them into synapses process obj
    fl_eps = get_fleps(nod_res)
    syn_proc.save_fleps(fl_eps)
    #Distribution of neurons
    try:
        nod_res = start_distribution(nod_dict,
                                     nod_dis_ep,
                                     synapses_process_id
                                    )
    except Exception as e:
        print(f"error during orchestration planning: {e}")

    return json.dumps(str(nod_res))

@app.route("/start_synapses_process", methods=['POST'])
def start_synapses_process():
    global syn_proc

    input_data = request.get_json()
    syn_proc = synapses_process(**input_data)

    synapses_process_id = id(syn_proc)
    syn_proc.set_object_memory_address(synapses_process_id)
    output = {"synapses_process_id": synapses_process_id}

    return json.dumps(output)

@app.route("/send_inputs_to_1layer_nods", methods=['POST'])
def send_inputs_to_1layer_nods():
    input_data = request.get_json()
    syn_proc = ctypes.cast(
        int(input_data["synapses_process_id"]),
        ctypes.py_object
    ).value
    nod_eps = syn_proc.read_fleps()
    start_first_layer_input_distribution(input_data,
                                         nod_eps)
    #json_data = json.dumps(input_data)
    #TODO: Change the following endpoint properly
    #headers = {'Content-type': 'application/json'}
    #result = requests.post("http://localhost:5000/send_nod_inputs",
    #                       data=json_data, headers=headers
    #                      )

    return result.text

@app.route("/set_final_output", methods=['POST'])
def set_final_output():
    input_data = request.get_json()
    syn_proc_id = get_synapses_obj_memory_address(
        input_data["synapses_process_id"]
    )
    #TODO: see if it's actually necessary to use syn_proc_id
    syn_proc = ctypes.cast(
        int(input_data["synapses_process_id"]),
        ctypes.py_object
    ).value
    syn_proc.set_synapses_output(input_data["inputs"])

    return "ok"

@app.route("/read_synapses_process_output", methods=['POST'])
def read_synapses_process_output():
    input_data = request.get_json()
    syn_proc = ctypes.cast(int(input_data["synapses_process_id"]), ctypes.py_object).value
    synapses_output = syn_proc.read_synapses_output()

    return synapses_output

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '7000')

    app.run(host=host, port=int(port))
