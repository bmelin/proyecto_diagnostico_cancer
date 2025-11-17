from flask import Flask, request, jsonify
from modelo_riesgo import calcular_riesgo

app = Flask(__name__)

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    resultado = calcular_riesgo(data)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(port=5000)
