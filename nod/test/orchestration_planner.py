import os
r][2])
                for j in range(0, neuron_num, neurons_per_nod):
                    nod_dict["nod_" + str(noc)] = save_nod_info_in_dict(
                        noc,
                        layer + 1,
                        info_layer[layer][0],
                        info_layer[layer][1][j:j+neurons_per_nod],
                        info_layer[layer][2][j:j+neurons_per_nod],
                        info_layer[layer][3][j:j+neurons_per_nod],
                        info_layer[layer][4][j:j+neurons_per_nod],
                        #current nod's ep
                        info_layer[layer][5][nod_ep_c],
                        #ep to the next neuron in next layer
                        info_layer[layer+1][5]
                    )
                    noc += 1
                    nod_ep_c += 1

        kwargs["nod_dict"] = nod_dict

        return kwargs

class OrchPlannerOps:

    @staticmethod
    def run(**kwargs):
        for operation in orc_pla_ops.__subclasses__():
            kwargs = operation.run_operation(**kwargs)

        return kwargs

