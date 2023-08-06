from flask import Flask, jsonify
from flask_cors import CORS

from flask.json import JSONEncoder
from plotly.utils import PlotlyJSONEncoder

from spintop.testplan.examples.fpga_translator_1 import get_fig
app = Flask(__name__)
CORS(app, supports_credentials=True)

class FlaskPlotlyJsonEncoder(JSONEncoder, PlotlyJSONEncoder):
    pass

app.json_encoder = FlaskPlotlyJsonEncoder

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/testplan/graph')
def get_graph():
    fig = get_fig()
    return jsonify(fig.to_dict())
    