# Create the nod classes
from . npu_cluster import NPUClusterOps

class nod():
    """ Define el nod procesador coordinador incluyendo sus atributos y metodos
    """

    def __init__(
        self,
        nod_id,
        pesos,
        biases,
        fas,
        capa_id,
        output_names,
        output_ip,
        output_port,
        input_names,
        input_num
    ):
        self.version = "1.0.0"
        self.nod_id = nod_id
        self.pesos = pesos
        self.biases = biases
        self.fas = fas
        self.capa_id = capa_id
        self.output_names = output_names
        self.output_ip = output_ip
        self.output_port = output_port
        self.input_names = input_names
        self.neuron_num = len(input_names)
        self.input_num = input_num
        self.inputs = {input_names[0]: [0 for i in range(self.input_num)]}
        self.input_num_count = 0
        self.status = "waiting"

        #self.instrucciones = self.get_format_instr(instrucciones) 
        #self.procesadores = self.get_format_proc(procesadores)

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
                output_ip = self.output_ip,
                output_port = self.output_port
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
            inpts = self.inputs[entrante_input_names[0]]
            for j, idx in enumerate(input_idx):
                inpts[idx] = inputs[entrante_input_names[0]][j]
                self.input_num_count += 1
            self.inputs[entrante_input_names[0]] = inpts
            if self.input_num == self.input_num_count:
                self.status = "ready"
            return True
        else:
            print("Inputs rejected")
            return False 


