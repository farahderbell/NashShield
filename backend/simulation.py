import numpy as np

def simulate_GBM(S0, mu, sigma, T, N):
    """
    Simule un sinistre via Brownien géométrique.
    """
    Z = np.random.normal(0, 1, N)
    ST = S0 * np.exp((mu - 0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)
    return ST

def calculer_profit(sinistres, quota):
    """
    Calcule le profit pour un assureur donné
    sinistres : array des sinistres simulés
    quota : quota de réassurance choisi (0-1)
    """
    profit = (1 - quota) * sinistres
    return profit

def simulation_3_assureurs(S0, mu, sigma, T, N, quotas):
    """
    Simulation pour 3 assureurs
    quotas : liste [q1, q2, q3]
    """
    sinistres = simulate_GBM(S0, mu, sigma, T, N)
    profit_A = calculer_profit(sinistres, quotas[0])
    profit_B = calculer_profit(sinistres, quotas[1])
    profit_C = calculer_profit(sinistres, quotas[2])
    return profit_A, profit_B, profit_C

def simulation_3_assureurs_different_claims(S0A, S0B, S0C, mu, sigma, T, N, quotas):
    """
    Simulation pour 3 assureurs avec claims différents
    S0A, S0B, S0C : initial claims pour chaque assureur
    quotas : liste [q1, q2, q3]
    """
    sinistres_A = simulate_GBM(S0A, mu, sigma, T, N)
    sinistres_B = simulate_GBM(S0B, mu, sigma, T, N)
    sinistres_C = simulate_GBM(S0C, mu, sigma, T, N)
    
    profit_A = calculer_profit(sinistres_A, quotas[0])
    profit_B = calculer_profit(sinistres_B, quotas[1])
    profit_C = calculer_profit(sinistres_C, quotas[2])
    return profit_A, profit_B, profit_C