import json

from flask import Flask, request
from nod.nod import nod

app = Flask(__name__)
nodo = None

@app.route("/")
def hello_world():
    return "<p>Hello, World! I'm a virtual NOD (Neuro Orchestrated Device)"+ \
           " running in EKS cluster in AWS as a pod. So I'm ready for running"+ \
           " multiple neurons. Nice to meet you.</p>"

@app.route("/save_neurons", methods=['POST'])
def save_neurons():
    global nodo
    nod_data = request.get_json()

    try:
        #print(nod_data)
        nodo = nod()
        if nodo.read_parameters(nod_data):
            if not nodo.save_parameteres(nod_data):
                raise Exception("Error saving parameters")
        else:
            raise Exception("Error reading parameters")
        result = {"result": "neurons installed"}
    except Exception as e:
        print(f"Error during getting nod parameters: {e}")
        result = {"result": f"error during getting nod params: {e}"}

    return json.dumps(result)


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')
    app.run(host=host, port=int(port))
