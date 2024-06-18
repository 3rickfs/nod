import os
import json
import ctypes

from flask import Flask, request
from nod.nod import nod

app = Flask(__name__)
nodo = None
outputs = []
#home = os.environ.get('HOME')
#if 'dev-1' in home:
    #app.config['UPLOAD_FOLDER'] = '/home/dev-1/dev/edge-intelligence-simulator/nod/nod/uploads'
#else:
#    app.config['UPLOAD_FOLDER'] = '/home/nod/nod/uploads'
try:
    pn = os.environ.get('POD_NAME')
    app.config['UPLOAD_FOLDER'] = "/nods_data/" + pn + "/uploads"
except:
    app.config['UPLOAD_FOLDER'] = os.getcwd() + "/uploads"

#Recreating the dict of synaptic processes
def recreate_synapses_processes():
    print("Recreating the synapses process file")
    p = app.config['UPLOAD_FOLDER']
    data = {}
    json_data = json.dumps(data)
    print(f"Synapses processes file will be saved in: {p}")
    with open(p + "/synapses_processes.json", "w+") as jf:
        json.dump(json_data, jf)
    jf.close()
    print("Recreation done")

recreate_synapses_processes()

def load_all_sp_nod_objs():
    try:
        fp = os.listdir(app.config['UPLOAD_FOLDER'])
        files = ["/sps/" + f for f in fp] #if os.path.isfile(f)]

        for f in files:
            with open(fp + f, "r") as jf:
                nod_data = json.load(jf)
            jf.close()

            nodo = nod()
            nodo_mem_adr = nodo.set_nodo_mem_adr(id(nodo),
                                                 nod_data["synapses_process_id"],
                                                 fp
                                                )
            r = nodo.read_parameters(nod_data)
            #get memory available
            #del nodo
    except Exception as e:
        raise Exception(f"Error loading saved synaptic processes: {e}")

def load_especific_nod_sp(spid):
    global nodo

    p = app.config['UPLOAD_FOLDER'] 
    files= os.listdir(p + "/sps")
    #print(f"fp: {fp}")
    #files = [f for f in fp if os.path.isfile(f)]

    nodo_mem_adr = 0
    for f in files:
        if str(spid) == f.split("-")[0]:
            with open(p + "/sps/" + f,"r") as jf:
                nod_data = json.load(jf)
            jf.close()

            nodo = nod()
            nodo_mem_adr = nodo.set_nodo_mem_adr(id(nodo),
                                                 spid,
                                                 p
                                                )
            r = nodo.read_parameters(nod_data)
            #print(f"loading nodo: {nodo.pesos}")

    return nodo_mem_adr

def delete_sp_nod_obj(nodo, spid):
    #Delete json file
    p = app.config['UPLOAD_FOLDER']
    os.remove(p + "/sps/" + nodo.spfn)

    #Delete registers
    p = app.config['UPLOAD_FOLDER']
    with open(p + "/synapses_processes.json", "r") as jf:
        sps = json.load(jf)
    jf.close()
    del sps[str(spid)] #nodo_obj_adr

    #Overwriting register
    with open(p + "/synapses_processes.json", "w") as jf:
        json.dump(sps, jf)
    jf.close()

def get_nod_sp(input_data):
    global nodo

    with open("synapses_processes.json", "r")  as jf:
        sps = json.load(jf)
    jf.close()

    sp = sps[str(input_data["synapses_process_id"])]
    dr = input_data["detailed_res"]
    if dr:
        res = sp
    else:
        res = sp["nod_id"]

    return res

def get_nodo_mem_adr(synapses_process_id):
    global nodo

    p = app.config['UPLOAD_FOLDER']
    with open(p + "/synapses_processes.json", "r") as jsonfile:
        sp = json.load(jsonfile)
    jsonfile.close()
    try:
        ma = sp[str(synapses_process_id)]
        print(f"NOD: the nodo mem adr is: {sp[str(synapses_process_id)]}")
    except Exception as e:
        print(f"No synaptic process found in RAM: {e}")
        print("Serching on disk")
        ma = load_especific_nod_sp(synapses_process_id)
        if ma == 0:
            print("No memory adr detected for underlying synaptic processes")

    return ma

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
                                             nod_data["synapses_process_id"],
                                             app.config["UPLOAD_FOLDER"]
                                            )
        #print("lalalal 1")
        #nod_data["nod_memory_address"] = nodo_mem_adr
        if nodo.read_parameters(nod_data):
            #if not nodo.save_parameters(nod_data):
            #    raise Exception("Error saving parameters")
            #else:
            # save the synaptic process in local persisten memory
            r = nodo.save_sp_nod_data(
                   app.config["UPLOAD_FOLDER"] + "/sps",
                   nod_data
                )
            if r != "ok":
                raise Exception(f"Error saving parameters: {e}")
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
            result = {"result": "nod inputs transferred",
                      "inputs_r": input_data['inputs']}
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
    global nodo

    input_data = request.get_json()
    #print(f"input data type: {type(input_data)}")
    #print(f"input data: {input_data}")
    #input_data = input_data.replace("\'", "\"")
    #input_data = json.loads(input_data)

    try:
        nodo_mem_adr = get_nodo_mem_adr(input_data["synapses_process_id"])
        if nodo_mem_adr == 0:
            raise Exception("Synaptic process id not found")
        nodo = ctypes.cast(int(nodo_mem_adr), ctypes.py_object).value
        #print(f"nodo input names: {nodo.input_names}")
        nodo.set_synapses_process_id(input_data["synapses_process_id"])
        #nodo.set_nod_destinations(input_data["nodo_mem_adr_dstn"])
        #reset input number counter
        #nodo.reset_input_num_count()
        #set initial inputs
        if nodo.set_inputs(input_data["inputs"],
                           input_data["input_idx"],
                           input_data["layer_id"]
                          ):
            result = {"result": "nod inputs transferred",
                      "inputs_r": input_data['inputs']}
            outputs = 123
        else:
            raise Exception("Error reading nod inputs")
    except Exception as e:
        print(f"Error reading nod inputs: {e}")
        result = {"result": f"error reading nod inputs: {e}"}

    return json.dumps(result)

@app.route("/get_sp_nod_info", methods=['POST'])
def get_sp_nod_info():
    input_data = request.get_json()

    try:
        res = get_nod_sp(input_data)
        result = {"result": res}

    except Exception as e:
        print(f"Error getting the sp nod info: {e}")
        result = {"result": f"Error getting the sp nod info: {e}"}

    return json.dumps(result)

@app.route("/remove_sp_nod_info", methods=['POST'])
def remove_sp_nod_info():
    input_data = request.get_json()

    nodo_mem_adr = get_nodo_mem_adr(input_data["synapses_process_id"])
    if nodo_mem_adr == 0:
        raise Exception("Synaptic process id not found")
    nodo = ctypes.cast(int(nodo_mem_adr), ctypes.py_object).value

    try:
        delete_sp_nod_obj(nodo, input_data["synapses_process_id"])
        del nodo
        res = {"result": "ok"}
    except Exception as e:
        print(f"Error removing sp nod info: {e}")
        res = {"result": "error"}

    return res

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')
    app.run(host=host, port=int(port))

