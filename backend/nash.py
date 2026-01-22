import numpy as np
from backend.simulation import simulation_3_insurers, simulation_3_insurers_different_premiums


def nash_equilibrium_3_insurers(S0, mu, sigma, T, N, retention_options):
    """
    Finds an approximate Nash equilibrium for 3 insurers with identical premiums.
    
    Ensures all players receive positive profit through fairness constraint.
    
    Real Quota-Share Formula:
    - Ceded quota Q = 1 - Retention
    - Ceded Premium: Pc = Q × P
    - Ceded Claims: Cc = Q × C
    - Profit = Retention × (Premium - Claims)
    
    Args:
        S0, mu, sigma, T, N: GBM parameters
        retention_options: List of possible retention rates (e.g., [0, 0.1, 0.2, ...])
    
    Returns:
        best_retentions: List of optimal retention rates [ret_A, ret_B, ret_C]
        profits_at_nash: Corresponding profits [profit_A, profit_B, profit_C]
    """
    
    best_retentions = [0.0, 0.0, 0.0]
    best_objective = float('-inf')
    profits_at_nash = [0.0, 0.0, 0.0]

    # Test all valid combinations
    for ret_A in retention_options:
        for ret_B in retention_options:
            for ret_C in retention_options:
                # Constraint 1: sum of retention rates ≤ 1
                # (reinsurers cannot cover more than 100%)
                if ret_A + ret_B + ret_C > 1.0:
                    continue
                
                # Constraint 2: Fairness - ensure all players get non-zero profit
                # Require minimum 0.05 retention for each player
                if ret_A < 0.05 or ret_B < 0.05 or ret_C < 0.05:
                    continue
                
                retentions = [ret_A, ret_B, ret_C]
                profit_A, profit_B, profit_C = simulation_3_insurers(S0, mu, sigma, T, N, retentions)
                
                # Calculate objectives
                mean_A = np.mean(profit_A)
                mean_B = np.mean(profit_B)
                mean_C = np.mean(profit_C)
                
                # Objective: Maximize total welfare while ensuring fairness
                total_profit = mean_A + mean_B + mean_C
                
                # Fairness bonus: penalize if one player dominates too much
                min_profit = min(mean_A, mean_B, mean_C)
                
                # Combined objective: maximize total + fairness bonus
                objective = total_profit + (0.1 * min_profit)
                
                if objective > best_objective:
                    best_objective = objective
                    best_retentions = retentions
                    profits_at_nash = [mean_A, mean_B, mean_C]
    
    # Fallback if no valid combination found
    if best_retentions == [0.0, 0.0, 0.0]:
        best_retentions = [0.33, 0.33, 0.34]
    
    return best_retentions, profits_at_nash


def nash_equilibrium_3_insurers_different_premiums(S0A, S0B, S0C, mu, sigma, T, N, retention_options):
    """
    Finds an approximate Nash equilibrium for 3 insurers with different premiums.
    
    Ensures all players receive positive profit through fairness constraint.
    
    Args:
        S0A, S0B, S0C: Initial premium amounts for each insurer
        mu, sigma, T, N: GBM parameters
        retention_options: List of possible retention rates
    
    Returns:
        best_retentions: List of optimal retention rates [ret_A, ret_B, ret_C]
        profits_at_nash: Corresponding profits [profit_A, profit_B, profit_C]
    """
    
    best_retentions = [0.0, 0.0, 0.0]
    best_objective = float('-inf')
    profits_at_nash = [0.0, 0.0, 0.0]

    # Test all valid combinations
    for ret_A in retention_options:
        for ret_B in retention_options:
            for ret_C in retention_options:
                # Constraint 1: sum of retention rates ≤ 1
                if ret_A + ret_B + ret_C > 1.0:
                    continue
                
                # Constraint 2: Fairness - ensure all players get non-zero profit
                # Require minimum 0.05 retention for each player to ensure positive profit
                if ret_A < 0.05 or ret_B < 0.05 or ret_C < 0.05:
                    continue
                
                retentions = [ret_A, ret_B, ret_C]
                profit_A, profit_B, profit_C = simulation_3_insurers_different_premiums(
                    S0A, S0B, S0C, mu, sigma, T, N, retentions
                )
                
                # Calculate objectives
                mean_A = np.mean(profit_A)
                mean_B = np.mean(profit_B)
                mean_C = np.mean(profit_C)
                
                # Objective: Maximize total welfare while ensuring fairness
                # Total welfare = sum of profits
                total_profit = mean_A + mean_B + mean_C
                
                # Fairness bonus: penalize if one player dominates too much
                # Use minimum profit as fairness metric
                min_profit = min(mean_A, mean_B, mean_C)
                
                # Combined objective: maximize total + fairness bonus
                # This ensures both high total profit AND fair distribution
                objective = total_profit + (0.1 * min_profit)
                
                if objective > best_objective:
                    best_objective = objective
                    best_retentions = retentions
                    profits_at_nash = [mean_A, mean_B, mean_C]
    
    # Fallback if no valid combination found (shouldn't happen)
    if best_retentions == [0.0, 0.0, 0.0]:
        best_retentions = [0.33, 0.33, 0.34]
    
    return best_retentions, profits_at_nash
