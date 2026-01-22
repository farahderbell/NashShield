import numpy as np

def simulate_GBM(S0, mu, sigma, T, N):
    """
    Simulates claims via Geometric Brownian Motion (GBM).
    S0: Initial premium or insured capital
    """
    Z = np.random.normal(0, 1, N)
    ST = S0 * np.exp((mu - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    return ST

def calculate_profit(premiums, claims, retention):
    """
    Calculates profit for an insurer under quota-share reinsurance.
    
    Real Quota-Share Formula:
    - Ceded Premium: Pc = Q × P  where Q = ceded quota (1 - retention)
    - Ceded Claims: Cc = Q × C  where Q = ceded quota
    - Insurer Profit = Retention × (P - C) = (1 - Q) × (P - C)
    
    Args:
        premiums: Array of premiums collected (P)
        claims: Array of claims paid (C)
        retention: Insurer's retention rate (0-1, % kept by primary insurer)
    
    Returns:
        profit: Array of profits calculated as retention × (premiums - claims)
    """
    profit = retention * (premiums - claims)
    return profit

def simulation_3_insurers(S0, mu, sigma, T, N, retentions):
    """
    Simulates quota-share reinsurance for 3 insurers with identical initial premiums.
    
    Args:
        S0: Initial premium amount (applies equally to all 3 insurers)
        mu, sigma, T, N: GBM parameters (drift, volatility, time horizon, simulations)
        retentions: List [ret_A, ret_B, ret_C] of retention rates for each insurer
    
    Returns:
        (profit_A, profit_B, profit_C): Arrays of simulated profits
    """
    # Generate premiums and claims for all 3 insurers
    premiums = simulate_GBM(S0, mu, sigma, T, N)
    # Claims = 70% of premiums (realistic loss ratio for insurance)
    claims = simulate_GBM(S0 * 0.7, mu, sigma, T, N)
    
    # Calculate profits using retention rates
    profit_A = calculate_profit(premiums, claims, retentions[0])
    profit_B = calculate_profit(premiums, claims, retentions[1])
    profit_C = calculate_profit(premiums, claims, retentions[2])
    return profit_A, profit_B, profit_C

def simulation_3_insurers_different_premiums(S0A, S0B, S0C, mu, sigma, T, N, retentions):
    """
    Simulates quota-share reinsurance for 3 insurers with different initial premiums.
    
    Args:
        S0A, S0B, S0C: Initial premium amounts for each insurer
        mu, sigma, T, N: GBM parameters (drift, volatility, time horizon, simulations)
        retentions: List [ret_A, ret_B, ret_C] of retention rates for each insurer
    
    Returns:
        (profit_A, profit_B, profit_C): Arrays of simulated profits
    """
    # Generate premiums and claims for each insurer independently
    premiums_A = simulate_GBM(S0A, mu, sigma, T, N)
    claims_A = simulate_GBM(S0A * 0.7, mu, sigma, T, N)
    
    premiums_B = simulate_GBM(S0B, mu, sigma, T, N)
    claims_B = simulate_GBM(S0B * 0.7, mu, sigma, T, N)
    
    premiums_C = simulate_GBM(S0C, mu, sigma, T, N)
    claims_C = simulate_GBM(S0C * 0.7, mu, sigma, T, N)
    
    # Calculate profits using retention rates
    profit_A = calculate_profit(premiums_A, claims_A, retentions[0])
    profit_B = calculate_profit(premiums_B, claims_B, retentions[1])
    profit_C = calculate_profit(premiums_C, claims_C, retentions[2])
    return profit_A, profit_B, profit_C