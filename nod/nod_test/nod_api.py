import json
import ctypes

from flask import Flask, request
from nod.nod import nod
#from synapses import synapses_process

app = Flask(__name__)
nodo = None
outputs = []

def get_nodo_mem_adr(synapses_process_id):
    with open("synapses_processes.json", "r") as jsonfile:
        sp = json.load(jsonfile)
    jsonfile.close()
    print(f"NOD: the nodo mem adr is: {sp[str(synapses_process_id)]}")

    return sp[str(synapses_process_id)]

@app.route("/")
def hello_world():
    return "<p>Hello, World! I'm a virtual NOD (Neuro Orchestrated Device)"+ \
           " running in an AWS EKS cluster as a pod. I'm now ready for running"+ \
           " multiple neurons. Nice to meet you.</p>"

@app.route("/save_neurons", methods=['POST'])
def save_neurons():
    global nodo
    nod_data = request.get_json()
    #TODO: review this type of handling coming strings
    #print(nod_data)
    #nod_data = nod_data.replace("\'", "\"")
    #print(nod_data)
    #print("------------------------------------")
    #print(type(nod_data))
    #nod_data = json.loads(nod_data)
    #print(f"nod_data: {nod_data}")

    try:
        nodo = nod()
        #print(f"nod_data: {nod_data['synapses_process_id']}")
        #nodo_mem_adr = nodo.set_synapses_process_id(id(nodo))
        nodo_mem_adr = nodo.set_nodo_mem_adr(id(nodo),
                                             nod_data["synapses_process_id"]
                                            )
        #print("lalalal 1")
        #nod_data["nod_memory_address"] = nodo_mem_adr
        if nodo.read_parameters(nod_data):
            if not nodo.save_parameters(nod_data):
                raise Exception("Error saving parameters")
        else:
            raise Exception("Error reading parameters")
        result = {"result": "neurons installed",
                  "nodo_mem_adr": nodo_mem_adr
                 }
    except Exception as e:
        print(f"Error during getting nod parameters: {e}")
        result = {"result": f"error during getting nod params: {e}"}
    
    #print("FINISHHED")
    return json.dumps(result)

@app.route("/set_nod_inputs", methods=['POST'])
def set_inputs():
    #global nodo, outputs
    input_data = request.get_json()

    try:
        nodo = ctypes.cast(int(input_data["nodo_mem_adr"]), ctypes.py_object).value
        if nodo.set_inputs(input_data["inputs"],
                           input_data["input_names"],
                           input_data["input_idx"],
                           input_data["layer_id"]
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

@app.route("/send_nod_inputs", methods=['POST'])
def send_nod_inputs():
    input_data = request.get_json()
    #print(f"input data type: {type(input_data)}")
    #print(f"input data: {input_data}")
    #input_data = input_data.replace("\'", "\"")
    #input_data = json.loads(input_data)

    try:
        nodo_mem_adr = get_nodo_mem_adr(input_data["synapses_process_id"])
        nodo = ctypes.cast(int(nodo_mem_adr), ctypes.py_object).value
        nodo.set_synapses_process_id(input_data["synapses_process_id"])
        #nodo.set_nod_destinations(input_data["nodo_mem_adr_dstn"])
        if nodo.set_inputs(input_data["inputs"],
                           input_data["input_names"],
                           input_data["input_idx"],
                           input_data["layer_id"]
                          ):
            result = {"result": "nod inputs transferred"}
            outputs = 123
        else:
            raise Exception("Error reading nod inputs")
    except Exception as e:
        print(f"Error reading nod inputs: {e}")
        result = {"result": f"error reading nod inputs: {e}"}

    return json.dumps(result)


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')
    app.run(host=host, port=int(port))

