import json

from flask import Flask
from nod.nod import nod  

app = Flask(__name__)
nod = None

@app.route("/")
def hello_world():
    return "<p>Hello, World! I'm a virtual NOD (Neuro Orchestrated Device)"+ \
           " running in EKS cluster in AWS as a pod. So I'm ready for running"+ \
           " multiple neurons. Nice to meet you.</p>"

@app.route("/save_neurons", methods=['POST'])
def save_neurons():
    global nod
    nod_data = request.get_json()

    try:
        nod = nod()
        if nod.read_parameters(nod_data):
            if not nod.save_parameteres(nod_data):
                raise Exception("Error saving parameters")
        else:
            raise Exception("Error reading parameters")
        result = {"result": "neurons installed"}
    except Exception as e:
        print(f"Error during getting nod parameters: {e}")
        result = {"result": "error during getting nod params: " + e}

    return json.dumps(result)


if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')
    app.run(host=host, port=int(port))
