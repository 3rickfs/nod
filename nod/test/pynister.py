import json
from flask import Flask, request

from orchestration_planner import read_endpoints, OrchPlannerOps

app = Flask(__name__)
syn_proc = None

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
    neuro_orchestrator_ep = ["http://localhost:5000/final_prediction"]
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
        #get lists of NOD objs mem addrss
        for l in range(len(nod_res)):
            mem_adrs = json.loads(nod_res[l].text)["syn_proc_id"]


    except Exception as e:
        print(f"error during orchestration planning: {e}")

    return json.dumps(nod_res)

@app.route("/start_synapses_process", methods=['POST'])
def start_synapses_process():
    global syn_proc

    input_data = request.get_json()
    syn_proc = synapses_process(**input_data)
    syn_proc_id = id(syn_proc)
    output = {"syn_prox_id": syn_proc_id}

    return json.dumps(syn_proc_id)

@app.route("/send_inputs_to_1layer_nods", methods=['POST'])
def send_inputs_to_1layer_nods():

    return []

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '7000')

    app.run(host=host, port=int(port))
