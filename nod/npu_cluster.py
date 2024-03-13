import os
from abc import ABC, abstractmethod
import json
import requests
import math

#import numpy as np

# softmax function
def softmax(z):
    # vector to hold exponential values
    exponents = []
    # vector to hold softmax probabilities
    softmax_prob = []
    # sum of exponentials
    exp_sum = 0
    # for each value in the input vector
    for value in z:
        # calculate the exponent
        exp_value = math.exp(value)
        # append to exponent vector
        exponents.append(exp_value)
        # add to exponential sum
        exp_sum += exp_value

    # for each exponential value
    for value in exponents:
        # calculate softmax probability
        probability = value / exp_sum
        # append to probability vector
        softmax_prob.append(probability)

    return softmax_prob

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
            #print(inpts)
            #print(kwargs["pesos"][i])
            mu = [x*w for w, x in zip(kwargs["pesos"][i], inpts)]
            m.append(mu)
        #print(m)
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

        #TODO: check if is worth the way of having different fa for each neuron
        for i in range(len(kwargs["sb"])):
            if kwargs["fas"][i] == "relu":
                kwargs["o"].append(max(0, kwargs["sb"][i]))

        #for now considering softmax for all the neurons of a layer in a NOD
        if kwargs["fas"][0] == "softmax":
            #x = np.array(kwargs["sb"])
            #ex = np.exp(x - np.max(x))
            #r = ex / ex.sum()
            #kwargs["o"] = [v for v in r] #np to list
            kwargs["o"] = softmax(kwargs["sb"])

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
        #print(output_msg)

        return kwargs

class execute_synapse(neuron_ops):
    """ send inputs to next nod
    """

    def run_operation(**kwargs):
        if kwargs["send_output_2_eps"]:
            print("Start synapse, sending inputs to next nod")

            nod_input = {
                "input_names": kwargs["output_names"],
                "inputs": kwargs["o"],
                #"input_idx": [i for i in range(len(kwargs["o"]))],
                "input_idx": [int(n[1:]) - 1 for n in kwargs["output_names"]],
                "synapses_process_id": kwargs["synapses_process_id"]
            }

            #for n in range(len(kwargs["output_ep"])):
            json_data = json.dumps(nod_input)
            headers = {'Content-type': 'application/json'}
            #print(f"output_eps: {kwargs['output_eps']}")
            #print(f"output_eps len: {len(kwargs['output_eps'])}")
            for oeps in range(len(kwargs["output_eps"])):
                #print(f"Sending synapse msg to: {kwargs['output_eps'][oeps]}")
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






