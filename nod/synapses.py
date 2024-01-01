
class synapses_process():
    def __init__(self, ai_model_path, distributed_model):
        self.ai_model_path = ai_model_path
        self.distributed_model = distributed_model
        self.mem_adr = 0
        self.synapses_output = []
        self.synapses_processes = {}
        self.synapses_process_id = 0

    def read_synapsys_output(self):
        print("Reading synpases output")
        return self.synapses_output

    def set_object_memory_address(self, nodo_ma):
        print("Saving object memory address into a dictionary")
        self.synapses_processes[str(nodo_ma)] = nodo_ma
        self.synapses_process_id = nodo_ma
        with open("synapses_processes.json", "w") as jsonfile:
            json.dump(json.dumps(str(self.synapses_processes)), jsonfile)
        jsonfile.close()

    def set_mem_adr(self, mem_adr):
        self.mem_adr = mem_adr

    def set_synapses_output(self, syn_output):
        self.synapses_output = syn_output

