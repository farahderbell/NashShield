from flask import Flask, render_template, request, jsonify
from backend.simulation import simulation_3_assureurs
import numpy as np
import os
# chemin absolu vers templates/ à la racine
template_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates')
static_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)

# Paramètres simulation
S0 = 1000
mu = 0.05
sigma = 0.2
T = 1
N = 10000

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    qA = float(data['qA'])
    qB = float(data['qB'])
    qC = float(data['qC'])
    
    profit_A, profit_B, profit_C = simulation_3_assureurs(S0, mu, sigma, T, N, [qA, qB, qC])
    
    result = {
        'profit_A': float(np.mean(profit_A)),
        'profit_B': float(np.mean(profit_B)),
        'profit_C': float(np.mean(profit_C))
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
