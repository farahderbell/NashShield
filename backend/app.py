from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from backend.simulation import simulation_3_insurers, simulation_3_insurers_different_premiums
from backend.nash import nash_equilibrium_3_insurers, nash_equilibrium_3_insurers_different_premiums
import numpy as np
import os
import math

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


# ===== SCR CALCULATION FUNCTIONS =====

class SCRCalculator:
    """Solvency Capital Requirement Calculator using Solvency II Standard Formula"""
    
    # Correlation matrix from custom specification (Marche, Contrepartie, Vie, Sante, Non Vie)
    CORRELATION_MATRIX = {
        'market': {'market': 1.0, 'counterparty': 0.25, 'life': 0.25, 'health': 0.25, 'nonlife': 0.25},
        'counterparty': {'market': 0.25, 'counterparty': 1.0, 'life': 0.25, 'health': 0.25, 'nonlife': 0.5},
        'life': {'market': 0.25, 'counterparty': 0.25, 'life': 1.0, 'health': 0.25, 'nonlife': 0.0},
        'health': {'market': 0.25, 'counterparty': 0.25, 'life': 0.25, 'health': 1.0, 'nonlife': 0.0},
        'nonlife': {'market': 0.25, 'counterparty': 0.5, 'life': 0.0, 'health': 0.0, 'nonlife': 1.0}
    }
    
    # Shock impact multipliers
    SHOCK_IMPACTS = {
        'market_interest_up': {'market': 1.085},
        'market_interest_down': {'market': 1.072},
        'market_equity_crash': {'market': 1.123},
        'market_property_decline': {'market': 1.068},
        'market_spread_widening': {'market': 1.091},
        'market_fx_volatility': {'market': 1.054},
        'life_mortality_shock': {'life': 1.042},
        'life_longevity_shock': {'life': 1.058},
        'life_lapse_shock': {'life': 1.035},
        'life_expense_shock': {'life': 1.021},
        'health_pandemic': {'health': 1.185},
        'health_premium_increase': {'health': 1.083},
        'health_claim_inflation': {'health': 1.067},
        'nonlife_nat_cat': {'nonlife': 1.225},
        'nonlife_man_cat': {'nonlife': 1.189},
        'nonlife_claims_inflation': {'nonlife': 1.094},
        'nonlife_reserve_shock': {'nonlife': 1.071},
        'combined_financial_crisis': {
            'market': 1.352, 'life': 1.125, 'health': 1.089, 'nonlife': 1.145, 'counterparty': 1.178
        },
        'combined_stress_test': {
            'market': 1.287, 'life': 1.089, 'health': 1.067, 'nonlife': 1.098, 'counterparty': 1.112
        },
        'combined_worst_case': {
            'market': 1.451, 'life': 1.256, 'health': 1.198, 'nonlife': 1.289, 'counterparty': 1.267
        }
    }
    
    @staticmethod
    def calculate_bscr(risk_values):
        """
        Calculate BSCR using custom correlation matrix formula.
        BSCR = √(Σ Σ ρ(i,j) × SCR(i) × SCR(j))
        """
        risks = ['market', 'life', 'health', 'nonlife', 'counterparty']
        bscr_squared = 0
        
        for i in risks:
            for j in risks:
                rho = SCRCalculator.CORRELATION_MATRIX[i][j]
                bscr_squared += rho * risk_values[i] * risk_values[j]
        
        bscr = math.sqrt(max(bscr_squared, 0))
        return bscr
    
    @staticmethod
    def calculate_scr(risk_values):
        """
        Calculate total SCR with operational risk.
        SCR = BSCR + Op Risk
        """
        bscr_components = {k: v for k, v in risk_values.items() if k != 'operational'}
        
        bscr = SCRCalculator.calculate_bscr(bscr_components)
        operational = risk_values.get('operational', 15)
        
        scr = bscr + operational
        
        return {
            'bscr': round(bscr, 2),
            'operational': round(operational, 2),
            'scr': round(scr, 2)
        }
    
    @staticmethod
    def apply_shock(risk_values, scenario_id):
        """
        Apply shock scenario to risk values.
        """
        if scenario_id not in SCRCalculator.SHOCK_IMPACTS:
            return {'error': f'Unknown scenario: {scenario_id}'}
        
        original = SCRCalculator.calculate_scr(risk_values)
        
        shocked_values = risk_values.copy()
        impacts = SCRCalculator.SHOCK_IMPACTS[scenario_id]
        
        for risk_type, multiplier in impacts.items():
            if risk_type in shocked_values:
                shocked_values[risk_type] = shocked_values[risk_type] * multiplier
        
        stressed = SCRCalculator.calculate_scr(shocked_values)
        
        impact_pct = ((stressed['scr'] - original['scr']) / original['scr'] * 100) if original['scr'] > 0 else 0
        
        return {
            'original_scr': original['scr'],
            'stressed_scr': stressed['scr'],
            'impact_amount': round(stressed['scr'] - original['scr'], 2),
            'impact_pct': round(impact_pct, 2),
            'stressed_values': {
                'market': round(shocked_values['market'], 2),
                'life': round(shocked_values['life'], 2),
                'health': round(shocked_values['health'], 2),
                'nonlife': round(shocked_values['nonlife'], 2),
                'counterparty': round(shocked_values['counterparty'], 2),
                'operational': round(shocked_values['operational'], 2)
            },
            'stressed_bscr': stressed['bscr'],
            'scenario': scenario_id
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/piliar1')
def piliar1():
    return render_template('piliar1.html')
@app.route('/piliar2')
def piliar2():
    return render_template('piliar2.html')
@app.route('/piliar3')
def piliar3():
    return render_template('piliar3.html')
@app.route('/fact')
def fact():
    return render_template('fact.html')

@app.route('/api/scr/calculate', methods=['POST'])
def calculate_scr():
    """
    Calculate SCR with given risk module values.
    
    Request JSON:
        - market: Market risk in M€ (float)
        - life: Life underwriting risk in M€ (float)
        - health: Health underwriting risk in M€ (float)
        - nonlife: Non-Life underwriting risk in M€ (float)
        - counterparty: Counterparty default risk in M€ (float)
        - operational: Operational risk in M€ (float)
    
    Response JSON:
        - bscr: Basic Solvency Capital Requirement
        - scr: Total Solvency Capital Requirement
        - operational: Operational risk component
    """
    try:
        data = request.get_json()
        
        risk_values = {
            'market': float(data.get('market', 50)),
            'life': float(data.get('life', 30)),
            'health': float(data.get('health', 20)),
            'nonlife': float(data.get('nonlife', 40)),
            'counterparty': float(data.get('counterparty', 10)),
            'operational': float(data.get('operational', 15))
        }
        
        result = SCRCalculator.calculate_scr(risk_values)
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        print(f"[ERROR] SCR Calculation Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/scr/shock', methods=['POST'])
def apply_scr_shock():
    """
    Apply shock scenario to SCR calculation.
    
    Request JSON:
        - market, life, health, nonlife, counterparty, operational: risk values
        - scenario: shock scenario ID (e.g., 'market_interest_up')
    
    Response JSON:
        - original_scr: SCR before shock
        - stressed_scr: SCR after shock
        - impact_amount: Change in SCR (M€)
        - impact_pct: Percentage change
        - stressed_values: Updated risk module values
        - stressed_bscr: BSCR after shock
    """
    try:
        data = request.get_json()
        
        risk_values = {
            'market': float(data.get('market', 50)),
            'life': float(data.get('life', 30)),
            'health': float(data.get('health', 20)),
            'nonlife': float(data.get('nonlife', 40)),
            'counterparty': float(data.get('counterparty', 10)),
            'operational': float(data.get('operational', 15))
        }
        
        scenario = data.get('scenario', 'market_interest_up')
        
        result = SCRCalculator.apply_shock(risk_values, scenario)
        
        if 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 400
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        print(f"[ERROR] SCR Shock Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/simulate', methods=['POST'])
def simulate():
    """
    API endpoint for quota-share reinsurance simulation.
    
    Real Formula:
    - Q = Ceded quota percentage (e.g., 0.7 = 70% ceded)
    - Retention = 1 - Q (percentage kept by primary insurer)
    - Prime cédée = Q × Prime (ceded premium)
    - Charge cédée = Q × Sinistre (ceded claim)
    - Profit = Retention × (Prime - Sinistre)
    
    Request JSON:
        - qA, qB, qC: retention rates for each insurer (0-1)
        - S0A, S0B, S0C: initial premiums for each insurer
        - scenario: 'classic' (user's choice) or 'nash' (equilibrium)
    
    Response JSON:
        - profit_A, profit_B, profit_C: mean expected profits
        - scenario: which scenario was run
    """
    try:
        print("\n[DEBUG] ===== NEW REQUEST =====")
        data = request.get_json()
        print(f"[DEBUG] Received JSON data: {data}")

        # Parse retention rates (0-1, representing % kept by insurer)
        retA = float(data.get('qA', 0))
        retB = float(data.get('qB', 0))
        retC = float(data.get('qC', 0))
        S0A = float(data.get('S0A', 1000))
        S0B = float(data.get('S0B', 1000))
        S0C = float(data.get('S0C', 1000))
        scenario = data.get('scenario', 'classic')
        
        print(f"[DEBUG] Parsed: retA={retA}, retB={retB}, retC={retC}, S0A={S0A}, S0B={S0B}, S0C={S0C}, scenario={scenario}")

        # Constraint: sum of retention rates ≤ 1
        # (retentions + ceded portions must sum to ≤ 1 across all parties)
        if retA + retB + retC > 1:
            print(f"[DEBUG] Constraint violation: sum={retA+retB+retC}")
            return jsonify({
                "error": "Sum of retention rates must be ≤ 1.0"
            }), 400

        if scenario == 'classic':
            print("[DEBUG] Running classic scenario (user-selected retentions)...")
            profit_A, profit_B, profit_C = simulation_3_insurers_different_premiums(
                S0A, S0B, S0C, mu, sigma, T, N, [retA, retB, retC]
            )
            print(f"[DEBUG] Classic done: A={len(profit_A)}, B={len(profit_B)}, C={len(profit_C)}")
            
        elif scenario == 'nash':
            print("[DEBUG] Running nash equilibrium scenario...")
            retention_options = [round(i * 0.1, 1) for i in range(11)]
            print(f"[DEBUG] Retention options: {retention_options}")
            print(f"[DEBUG] Starting nash_equilibrium calculation...")
            best_retentions, profits_nash = nash_equilibrium_3_insurers_different_premiums(
                S0A, S0B, S0C, mu, sigma, T, N, retention_options
            )
            print(f"[DEBUG] Nash done: retentions={best_retentions}, profits={profits_nash}")
            profit_A, profit_B, profit_C = simulation_3_insurers_different_premiums(
                S0A, S0B, S0C, mu, sigma, T, N, best_retentions
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

