# Create the nod classes
import json

from . npu_cluster import NPUClusterOps

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
        self.input_num_count = 0
        self.status = "waiting"

        #self.instrucciones = self.get_format_instr(instrucciones) 
        #self.procesadores = self.get_format_proc(procesadores)

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

            #TODO: validate most critic parameters
        except Exception as e:
            return False

        return True

    def save_parameteres(self, nod_data):
        print("Saving parameters as json format")
        try:
            with open("./nod_ai_model.json","w") as jsonfile:
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
                output_eps = self.output_eps
            )
            self.status = "waiting" #for next job
            self.input_num_count = 0
        except Exception as e:
            result = {
                'error': e
            }

        return result

    def verify_input(self, entrante_input_names, input_idx):
        if self.input_names == entrante_input_names:
            return True
        else:
           return False

    def set_inputs(self, inputs, entrante_input_names, input_idx):
        if self.verify_input(entrante_input_names, input_idx):
            print("Inputs accepted")
            inpts = self.inputs
            for j, idx in enumerate(input_idx):
                inpts[idx] = inputs[j]
                self.input_num_count += 1
            self.inputs = inpts
            if self.input_num == self.input_num_count:
                self.status = "ready"
            return True
        else:
            print("Inputs rejected")
            return False


