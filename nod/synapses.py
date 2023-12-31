
class synapses_process():
    def __init__(self, ai_model_path, distributed_model):
        self.ai_model_path = ai_model_path
        self.distributed_model = distributed_model
        self.mem_adr = 0
        self.synapses_output = []

    def set_mem_adr(self, mem_adr):
        self.mem_adr = mem_adr

    def set_synapses_output(self, syn_output):
        self.set_synapses_output = syn_output

