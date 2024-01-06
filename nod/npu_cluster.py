import os
from abc import ABC, abstractmethod
import json
import requests

class neuron_ops(ABC):
    """
    """

    @abstractmethod
    def run_operation(**kwargs):
        #interface to child classes
        pass


class mul_vectors(neuron_ops):
    """ multiplicar vector de entradas con vector de pesos
    """

    def run_operation(**kwargs):
        print("Multiplicar vector x con w")
        m = []
        inpts = kwargs["inputs"]
        for i in range(len(kwargs["pesos"])):
            #print(kwargs["inputs"]["i1"][i])
            print(inpts)
            print(kwargs["pesos"][i])
            mu = [x*w for w, x in zip(kwargs["pesos"][i], inpts)]
            m.append(mu)
        print(m)
        kwargs["m"] = m

        return kwargs

class sum_vectors(neuron_ops):
    """ Sumar elementos del vector resultante de la multiplicacion
    """

    def run_operation(**kwargs):
        print("Sumar elementos del vector")
        kwargs["s"] = []
        for i in range(len(kwargs["m"])):
            kwargs["s"].append(sum(kwargs["m"][i]))

        return kwargs

class apply_bias(neuron_ops):
    """ Aplicar el bias
    """

    def run_operation(**kwargs):
        print("Aplicar bias")
        kwargs["sb"] = []
        for i in range(len(kwargs["s"])):
            #print(f"s {kwargs['s']}")
            #print(f"biases {kwargs['biases']}")
            kwargs["sb"].append(kwargs["s"][i] + kwargs["biases"][i])

        return kwargs

class apply_fa(neuron_ops):
    """ Aplicar la funcion de activacion
    """

    def run_operation(**kwargs):
        print("Aplicar la funcion de activacion")
        kwargs["o"] = []
        for i in range(len(kwargs["sb"])):
            if kwargs["fas"][i] == "relu":
                kwargs["o"].append(max(0, kwargs["sb"][i]))
                #TODO: code softmax function

        return kwargs


class success_msg(neuron_ops):
    """ Generar mensaje de exito
    """

    def run_operation(**kwargs):
        print("Generar mensaje de exito")
        kwargs["result"] = "Successful"

        return kwargs

class create_output_msgs(neuron_ops):
    """ Crear mensajes de salida para los destinos correspondientes
    """

    def run_operation(**kwargs):
        print("Crear mensajes de salida")
        output_msg = {
            'input_names': kwargs["output_names"],
            'inputs': kwargs["o"]
        }
        kwargs["output_msg"] = output_msg
        print(output_msg)

        return kwargs

class execute_synapse(neuron_ops):
    """ send inputs to next nod
    """

    def run_operation(**kwargs):
        print("Start synapse, sending inputs to next nod")

        nod_input = {
            "input_names": kwargs["output_names"],
            "inputs": kwargs["o"],
            #TODO: fix this input_idx thing to have proper values according to output_names
            "input_idx": [i for i in range(len(kwargs["o"]))],
            "synapses_process_id": kwargs["synapses_process_id"]
        }

        #TODO: consider more than one output endpoint
        #for n in range(len(kwargs["output_ep"])):
        json_data = json.dumps(nod_input)
        headers = {'Content-type': 'application/json'}
        print(f"output_eps: {kwargs['output_eps']}")
        print(f"output_eps len: {len(kwargs['output_eps'])}")
        for oeps in range(len(kwargs["output_eps"])):
            print("entro")
            print(f"Sending synapse msg to: {kwargs['output_eps'][oeps]}")
            result = requests.post(kwargs["output_eps"][oeps],
                                   data=json_data, headers=headers
                                  )

        return kwargs


class NPUClusterOps:

    @staticmethod
    def run(**kwargs):
        for operation in neuron_ops.__subclasses__():
            kwargs = operation.run_operation(**kwargs)

        return kwargs






