import json
from flask import Flask, request

from orchestration_planner import read_endpoints, OrchPlannerOps

app = Flask(__name__)

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

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')

    app.run(host=host, port=int(port))
