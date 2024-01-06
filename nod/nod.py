# Create the nod classes
import json

from npu_cluster import NPUClusterOps

class nod():
    """ Define el nod procesador coordinador incluyendo sus atributos y metodos
    """

    def __init__(
        self
        #nod_id="",
        #pesos=[],
        #biases=[],
        #fas=[],
        #capa_id="",
        #output_names=[],
        #output_ip=[],
        #output_port=[],
        #output_eps=[],
        #input_names=[]
    ):
        self.version = "1.0.0"
        self.nod_id = ""
        self.pesos = []
        self.biases = []
        self.fas = []
        self.capa_id = ""
        self.output_names = []
        #self.output_ip = output_ip
        #self.output_port = output_port
        self.output_eps = []
        self.input_names = []
        self.neuron_num = len(self.output_names)
        self.input_num = len(self.input_names)
        self.inputs = [0 for i in range(self.input_num)]
        self.neuron_outputs = [0 for i in range(len(self.pesos))]
        self.input_num_count = 0
        self.status = "waiting"
        #self.nod_memory_address = ""
        self.nodo_mem_adr_dstn = ""
        self.synapses_process_id = 0
        self.synapses_processes = dict()

        #self.instrucciones = self.get_format_instr(instrucciones) 
        #self.procesadores = self.get_format_proc(procesadores)

    def set_nodo_mem_adr(self, nodo_ma, synapses_process_id):
        print("Saving object memory address into a dictionary")
        print(f"synpasys process id: {str(synapses_process_id)}")
        self.synapses_processes[str(synapses_process_id)] = nodo_ma
        print(f"nodo ma: {nodo_ma}")
        self.synapses_process_id = synapses_process_id
        with open("synapses_processes.json", "w") as jsonfile:
            #json.dump(json.dumps(str(self.synapses_processes)), jsonfile)
            json.dump(self.synapses_processes, jsonfile)
        jsonfile.close()

        return nodo_ma

    def set_synapses_process_id(self, synapses_process_id):
        print("Setting the synapses process id")
        self.synapses_process_id = synapses_process_id

    def get_neuron_outputs(self):
        print("Getting neuron outputs")
        return self.neuron_outputs

    def read_parameters(self, nod_data):
        print("Reading nod parameters")
        try:
            self.nod_id = nod_data["nod_id"]
            self.capa_id = nod_data["capa_id"]
            self.input_names = nod_data["input_names"]
            self.pesos = nod_data["pesos"]
            self.biases = nod_data["biases"]
            self.fas = nod_data["fas"]
            self.output_names = nod_data["output_names"]
            self.output_eps = nod_data["output_ep"]
            self.neuron_num = len(self.output_names)
            self.input_num = len(self.input_names)
            self.inputs = [0 for i in range(self.input_num)]
            self.neuron_outputs = [0 for i in range(len(self.pesos))]
            #self.nod_memory_address = nod_data["nod_memory_address"]
            self.synapses_process_id = nod_data["synapses_process_id"]

            #TODO: validate most critic parameters
        except Exception as e:
            return False

        return True

    def save_parameters(self, nod_data):
        print("Saving parameters as json format")
        try:
            #TODO: update following file path according to real nods
            with open("./nod_ai_model.json","w") as jsonfile:
                #json.dump(json.dumps(str(nod_data)), jsonfile)
                print(f"Saving nod_data: {type(nod_data)}")
                json.dump(nod_data, jsonfile)
            jsonfile.close()

        except Exception as e:
            print(e)
            return False

        return True

    def run_neuron_ops(self):
        print("Running the neurons, muchachon!")
        try:
            result = NPUClusterOps.run(
                inputs = self.inputs,
                pesos = self.pesos,
                biases = self.biases,
                fas = self.fas,
                input_names = self.input_names,
                output_names = self.output_names,
                #output_ip = self.output_ip,
                #output_port = self.output_port
                output_eps = self.output_eps,
                synapses_process_id = self.synapses_process_id
            )
            self.neuron_outputs = result["o"]
            self.status = "waiting" #for next job
            self.input_num_count = 0
        except Exception as e:
            result = {
                'error': e
            }

        return result

    def verify_input(self, entrante_input_names):
        res = False
        for ein in entrante_input_names:
            if ein in self.input_names:
                res = True
            else:
                return False
        return res

    def set_inputs(self, inputs, entrante_input_names, input_idx):
        if self.verify_input(entrante_input_names):
            print("Inputs accepted")
            inpts = self.inputs
            for j, idx in enumerate(input_idx):
                inpts[idx] = inputs[j]
                self.input_num_count += 1
            self.inputs = inpts
            if self.input_num == self.input_num_count:
                self.status = "ready"
                #Running neurons inmediately after setting inputs
                r = self.run_neuron_ops()
                self.input_num_count = 0
            return True
        else:
            print("Inputs rejected")
            return False


