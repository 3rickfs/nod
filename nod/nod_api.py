import json
import ctypes

from flask import Flask, request
from nod.nod import nod

app = Flask(__name__)
nodo = None
outputs = []

@app.route("/")
def hello_world():
    return "<p>Hello, World! I'm a virtual NOD (Neuro Orchestrated Device)"+ \
           " running in EKS cluster in AWS as a pod. So I'm ready for running"+ \
           " multiple neurons. Nice to meet you.</p>"

@app.route("/save_neurons", methods=['POST'])
def save_neurons():
    global nodo
    nod_data = request.get_json()

    try:
        nodo = nod()
        nodo_mem_adr = id(nodo)
        nod_data["nod_memory_address"] = nodo_mem_adr
        if nodo.read_parameters(nod_data):
            if not nodo.save_parameteres(nod_data):
                raise Exception("Error saving parameters")
        else:
            raise Exception("Error reading parameters")
        result = {"result": "neurons installed",
                  "nodo_mem_adr": nodo_mem_adr
                 }
    except Exception as e:
        print(f"Error during getting nod parameters: {e}")
        result = {"result": f"error during getting nod params: {e}"}

    return json.dumps(result)

@app.route("/set_nod_inputs", methods=['POST'])
def set_inputs():
    #global nodo, outputs
    input_data = request.get_json()

    try:
        nodo = ctypes.cast(int(input_data["nodo_mem_adr"]), ctypes.py_object).value
        if nodo.set_inputs(input_data["inputs"],
                           input_data["input_names"],
                           input_data["input_idx"]
                          ):
            result = {"result": "nod inputs transferred"}
            outputs = 123
        else:
            raise Exception("Error reading nod inputs")
    except Exception as e:
        print(f"Error reading nod inputs: {e}")
        result = {"result": f"error reading nod inputs: {e}"}

    return json.dumps(result)

@app.route("/get_neuron_outputs", methods=['POST'])
def get_neuron_outputs():
    #global nodo, outputs
    input_data = request.get_json()

    try:
        nodo = ctypes.cast(int(input_data["nodo_mem_adr"]), ctypes.py_object).value
        neuron_outputs = nodo.get_neuron_outputs()
    except Exception as e:
        print(f"Error getting the neuron outputs: {e}")
        neuron_outputs = 0

    return str(neuron_outputs)


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')
    app.run(host=host, port=int(port))
