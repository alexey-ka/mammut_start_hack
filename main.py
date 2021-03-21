import json
import flask
import data_analysis

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

@app.route('/vertical', methods=['GET'])
def home():
    result = data_analysis.make_analysis()

    response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run()