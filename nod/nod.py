# Create the nod classes
import json

from nod.npu_cluster import NPUClusterOps

class nod():
    """ Define el nod procesador coordinador incluyendo sus atributos y metodos
    """

    def __init__(
        self
        #nod_id="",
        #pesos=[],
        #biases=[],
        #fas=[],
        #dsapa_id="",
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
        self.capa_ids = ""
        self.output_names = []
        #self.output_ip = output_ip
        #self.output_port = output_port
        self.output_eps = []
        self.input_names = []
        #self.neuron_num = len(self.output_names)
        self.input_num = len(self.input_names)
        self.inputs = [0 for i in range(self.input_num)]
        self.neuron_outputs = [] 
        self.input_num_count = []
        self.status = "waiting"
        #self.nod_memory_address = ""
        self.nodo_mem_adr_dstn = ""
        self.synapses_process_id = 0
        self.synapses_processes = dict()
        self.so2eps = []
        self.flid = 0
        self.finns = []
        self.verbose = False
        self.spfn = ""

        #self.instrucciones = self.get_format_instr(instrucciones) 
        #self.procesadores = self.get_format_proc(procesadores)

    def save_sp_nod_data(self, sps_folder_path, nod_data):
        print("Saving synaptic process nod data")
        spfn = nod_data["synapses_process_id"] + "-" + str(nod_data["mfname"])
        self.spfn = spfn
        with open(sps_folder_path + "/" + spfn, "w") as jf:
            json.dump(nod_data, jf)
        jf.close()


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

            self.capa_ids = nod_data["capa_ids"]
            sn = int(nod_data["i"][0][0][1:])
            en = int(nod_data["i"][1][0][1:])
            fl = nod_data["i"][0][0] #first letter
            self.input_names = [fl + str(i) for i in range(sn, en + 1)]
            self.pesos = nod_data["p"]
            self.biases = nod_data["b"]
            self.fas = nod_data["f"]
            sn = int(nod_data["o"][0][0][1:])
            en = int(nod_data["o"][1][0][1:])
            fl = nod_data["o"][0][0] #first letter
            self.output_names = [fl + str(i) for i in range(sn, en + 1)] #nod_data["o"]
            self.output_eps = nod_data["output_eps"]
            self.finns = nod_data["finns"]
            #self.neuron_num = len(self.output_names)
            #len(self.input_names)
            self.input_num = nod_data["input_num"] #[len(w[0]) for w in self.pesos]
            #self.inputs = [0 for i in range(self.input_num[0])] #first layer
            self.inputs = []
            self.input_num_count = []
            for l in self.input_num: #for all layers
                zeros = [0 for i in range(l)]
                self.inputs.append(zeros.copy())
                self.input_num_count.append(zeros.copy())
            if self.verbose:
                print(f"input num: {self.input_num}")
                print(f"input num count: {self.input_num_count}")
                for i in range(len(self.input_num_count)):
                    print(f"input num count len: {len(self.input_num_count[i])}")
            #print(f"set up inputs: {self.inputs}")
            #self.neuron_outputs = [0 for i in range(len(self.pesos))]
            #self.nod_memory_address = nod_data["nod_memory_address"]
            self.synapses_process_id = nod_data["synapses_process_id"]
            self.so2eps = [False for i in range(len(self.capa_ids))]
            self.so2eps[-1] = True
            self.flid = self.capa_ids[0]

            #TODO: validate most critic parameters
        except Exception as e:
            print(f"error reading parameters: {e}")
            return False

        return True

    def save_parameters(self, nod_data):
        print("Saving parameters as json format")
        try:
            #TODO: update following file path according to real nods
            with open("./nod_ai_model.json","w") as jsonfile:
                #json.dump(json.dumps(str(nod_data)), jsonfile)
                #print(f"Saving nod_data: {type(nod_data)}")
                json.dump(nod_data, jsonfile)
            jsonfile.close()

        except Exception as e:
            print(e)
            return False

        return True

    def run_neuron_ops(self, layer_id):
        print("Running all the neurons, muchachon!")
        lid = 0
        try:
            while True:
                indx = layer_id + lid
                lnum = len(self.capa_ids)
                so2e = False
                #if indx < len(self.output_eps) 
                if self.output_eps[indx] != []:
                    so2e = True
                result = NPUClusterOps.run(
                    inputs = self.inputs[indx],
                    pesos = self.pesos[indx],
                    biases = self.biases[indx],
                    fas = self.fas[indx],
                    #input_names = self.input_names, #from first layer
                    layer_id = self.capa_ids[indx],
                    output_names = self.output_names[indx],
                    #output_ip = self.output_ip,
                    #output_port = self.output_port
                    output_eps = self.output_eps[indx],
                    synapses_process_id = self.synapses_process_id,
                    send_output_2_eps = so2e #TODO: self.so2eps[indx] #False #what happens if this is for the same nod
                )
                if lnum > 1 and indx < lnum - 1:
                    lid += 1 #next layer
                    indx = layer_id + lid
                    if self.input_num[indx] == len(result["o"]):
                        self.inputs[indx] = result["o"]
                        #self.input_idx = [int(n[1:]) - 1 for n in self.output_names[layer_id+lid]]
                    else:
                        #frm = int(self.output_names[indx-1][0][1:])
                        #to = len(self.output_names[indx])
                        #print("ENTRAMOS AQUII")
                        #i1 = int(self.output_names[indx-1][0][1:])
                        #i2 = int(self.input_names[indx][0][1:])
                        #print(f"i1: {i1}, i2: {i2}")
                        #previous layer's output names is the input of the next
                        #being part of neurons only processed by current nod
                        i1 = int(self.output_names[indx-1][0][1:])
                        frm =  i1 - self.finns[indx]
                        #print("KAKAKAKAKAKAK")
                        i2 = int(self.output_names[indx-1][-1][1:])
                        to = i2 - self.finns[indx] + 1
                        self.inputs[indx][frm:to] = result["o"]
                        ones = [1 for i in result["o"]]
                        self.input_num_count[indx][frm:to] = ones
                        if self.verbose:
                            print(f"i1: {i1}, i2: {i2}")
                            print(f"from: {frm}, to: {to}")
                            print(f"index: {indx}")
                            print(f"inputs len: {len(self.inputs[indx])}")
                            print(f"input num count len: {len(self.input_num_count[indx])}")
                            print(f"printing inputs: {self.inputs[indx]}")
                        #Make sure the inputs are complete if so run the next layer
                        if 0 in self.input_num_count[indx]:
                            break
                else:
                    break

            self.neuron_outputs = result["o"]
            self.status = "waiting" #for next job
            #self.input_num_count[layer_id] = 0
        except Exception as e:
            result = {
                'error': e
            }

        return result

    def verify_input(self, entrante_input_names, layer_id):
        res = False
        for ein in entrante_input_names:
            if ein in self.input_names[layer_id]:
                res = True
            else:
                return False
        return res

    def set_inputs(self, inputs, input_idx, layer_id):
        indx = layer_id - self.flid
        if self.verbose: print(f"IIIIINNNNDEEXX: {indx}")
        #if self.verify_input(indx):
        inpts = self.inputs[indx]
        iz = len(inputs)
        if self.verbose:
            print("Inputs accepted")
            print(f"coming inputs: {inputs}")
            print(f"indx: {indx}")
            #print(f"inputs: {self.inputs}")
            print(f"layer id: {layer_id}")
            print(f"inpts size: {iz}")
            print(f"inputs size: {len(inputs)}")
            print(f"input idx: {input_idx}")
            #print(f"input names: {self.input_names}")
            #print(f"inputn_names[0][1:]: {int(self.input_names[0][0][1:])}")
            print(f"input num count: {self.input_num_count[indx]}")
            print(f"input num count len: {len(self.input_num_count[indx])}")
        for j in range(len(inputs)):
                #print(f"idx: {idx}")
                #print(f"j: {j}")
                #inpts[idx] = inputs[j]
            i = input_idx + j - int(self.input_names[indx][0][1:]) + 1
            #print(f"i: {i}")
            #print(f"selected input: {inputs[j]}")
            inpts[i] = inputs[j]
            ii = input_idx - self.finns[indx] + 1 + j
            if self.verbose:
                print(ii)
                print(f"finns: {self.finns[indx]}")
            self.input_num_count[indx][ii] = 1
        self.inputs[indx] = inpts
        if self.verbose:
            print(f"inpts: {inpts}")
            print(f"input num count: {self.input_num_count[indx]}")

        #if self.input_num[indx] == self.input_num_count[indx]:
        #for l in : #for all layers
        if not 0 in self.input_num_count[indx]:
            #print(f"Ready for running the models with following inpunts: {self.inputs}")
            self.status = "ready" #TODO: integrate nod's status management
            zeros = [0 for i in range(self.input_num[layer_id])]
            self.input_num_count[indx] = zeros
            #Running neurons inmediately after setting inputs
            r = self.run_neuron_ops(indx)
        return True
        #else:
        #    print("Inputs rejected")
        #    return False


