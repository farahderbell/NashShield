from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from backend.simulation import simulation_3_assureurs, simulation_3_assureurs_different_claims
from backend.nash import nash_equilibrium_3_assureurs, nash_equilibrium_3_assureurs_different_claims
import numpy as np
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_path = os.path.join(BASE_DIR, 'templates')
static_path = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
CORS(app)

# Simulation parameters
S0 = 1000
mu = 0.05
sigma = 0.2
T = 1
N = 1000  # Reduced from 10000 for better performance

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        print("\n[DEBUG] ===== NEW REQUEST =====")
        data = request.get_json()
        print(f"[DEBUG] Received JSON data: {data}")

        qA = float(data.get('qA', 0))
        qB = float(data.get('qB', 0))
        qC = float(data.get('qC', 0))
        S0A = float(data.get('S0A', 1000))
        S0B = float(data.get('S0B', 1000))
        S0C = float(data.get('S0C', 1000))
        scenario = data.get('scenario', 'classic')
        
        print(f"[DEBUG] Parsed: qA={qA}, qB={qB}, qC={qC}, S0A={S0A}, S0B={S0B}, S0C={S0C}, scenario={scenario}")

        # Quota-share constraint
        if qA + qB + qC > 1:
            print(f"[DEBUG] Constraint violation: sum={qA+qB+qC}")
            return jsonify({
                "error": "Sum of quota-shares must be ≤ 1."
            }), 400

        if scenario == 'classic':
            print("[DEBUG] Running classic scenario...")
            profit_A, profit_B, profit_C = simulation_3_assureurs_different_claims(
                S0A, S0B, S0C, mu, sigma, T, N, [qA, qB, qC]
            )
            print(f"[DEBUG] Classic done: A={len(profit_A)}, B={len(profit_B)}, C={len(profit_C)}")
            
        elif scenario == 'nash':
            print("[DEBUG] Running nash scenario...")
            quotas_options = [round(i * 0.1, 1) for i in range(11)]
            print(f"[DEBUG] Quota options: {quotas_options}")
            print(f"[DEBUG] Starting nash_equilibrium calculation...")
            best_quotas, profits_nash = nash_equilibrium_3_assureurs_different_claims(
                S0A, S0B, S0C, mu, sigma, T, N, quotas_options
            )
            print(f"[DEBUG] Nash done: quotas={best_quotas}, profits={profits_nash}")
            profit_A, profit_B, profit_C = simulation_3_assureurs_different_claims(
                S0A, S0B, S0C, mu, sigma, T, N, best_quotas
            )
            print(f"[DEBUG] Final simulation done")
        else:
            return jsonify({"error": "Invalid scenario."}), 400

        import numpy as np
        result = {
            "profit_A": float(np.mean(profit_A)),
            "profit_B": float(np.mean(profit_B)),
            "profit_C": float(np.mean(profit_C)),
            "scenario": scenario,
            "message": f"Simulation completed for scenario: {scenario}"
        }
        
        print(f"[DEBUG] Result: {result}")
        return jsonify(result)

    except Exception as e:
        print(f"\n[ERROR] Exception in simulate!")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
