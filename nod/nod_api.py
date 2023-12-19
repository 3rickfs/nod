from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World! I'm a virtual NOD (Neuro Orchestrated Device) running in EKS cluster in AWS as a pod. So I'm ready for running multiple neurons. Nice to meet you.</p>"

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5000')
    app.run(host=host, port=int(port))
