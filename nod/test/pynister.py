import json
from flask import Flask, request

from orchestration_planner import read_endpoints, OrchPlannerOps

app = Flask(__name__)
syn_proc = None

def get_synapses_obj_memory_address(synapses_process_id):
    print("Getting synapses object memory address")
    with open("synapses_processes.json", "r") as jsonfile:
        self.synapses_processes = json.load(jsonfile)
    jsonfile.close()
    return self.synapses_processes[str(synapses_process_id)]

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
    #this will be used for the neuro orchestrator to send json to nods too
    #nod_ep = read_endpoints("./nod_endpoints.txt")
    #this EP are to share ops info btw NODs
    nod_ops_ep = read_endpoints(json_data["nod_ops_endpoints"])
    #Need other EP to send neuorns info from NO to NODs
    nod_dis_ep = read_endpoints(json_data["nod_dis_endpoints"])
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
    #Distribution of neurons
    try:
        nod_res = neuron_distributor.start_distributon(nod_dict,
                                                       nod_dis_ep
                                                      )
    except Exception as e:
        print(f"error during orchestration planning: {e}")

    return json.dumps(nod_res)

@app.route("/start_synapses_process", methods=['POST'])
def start_synapses_process():
    global syn_proc

    input_data = request.get_json()
    syn_proc = synapses_process(**input_data)

    synapses_process_id = id(syn_proc)
    syn_proc.set_synapses_process_id(synapses_process_id)
    output = {"synapses_process_id": synapses_process_id}

    return json.dumps(syn_proc_id)

@app.route("/send_inputs_to_1layer_nods", methods=['POST'])
def send_inputs_to_1layer_nods():

    input_data = request.get_json()

    json_data = json.dumps(input_data)
    #TODO: Change the following endpoint properly
    result = requests.post("http://localhost:5000/send_nod_inputs",
                           data=json_data, headers=headers
                          )

    return result.text

@app.route("/set_final_output", methods=['POST'])
def set_final_output():
    input_data = request.get_json()
    syn_proc_id = get_synapses_obj_memory_address(
        input_data["synapses_process_id"]
    )
    #TODO: see if it's actually necessary to use syn_proc_id
    syn_proc = ctypes.cast(int(input_data["synapses_process_id"]), ctypes.py_object).value
    syn_proc.set_synapses_output(input_data["final_output"])

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
