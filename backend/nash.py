import numpy as np
from backend.simulation import simulation_3_assureurs


def nash_equilibrium_3_assureurs(S0, mu, sigma, T, N, quotas_options):
    """
    Trouve un équilibre de Nash pour 3 assureurs en testant différentes combinaisons de quotas.
    
    Args:
        S0, mu, sigma, T, N : paramètres GBM
        quotas_options : liste de quotas possibles pour chaque assureur (ex : [0.2, 0.4, 0.6, 0.8])
    
    Returns:
        best_quotas : liste des quotas au Nash equilibrium [qA, qB, qC]
        profits_at_nash : profits correspondants [profit_A, profit_B, profit_C]
    """
    
    best_quotas = [0.0, 0.0, 0.0]
    profits_at_nash = [0.0, 0.0, 0.0]

    # Pour l'instant on fait un simple essai : toutes les combinaisons possibles
    for qA in quotas_options:
        for qB in quotas_options:
            for qC in quotas_options:
                quotas = [qA, qB, qC]
                profit_A, profit_B, profit_C = simulation_3_assureurs(S0, mu, sigma, T, N, quotas)
                
                # Pour le moment, on stocke juste la combinaison qui maximise la somme des profits
                total_profit = np.mean(profit_A) + np.mean(profit_B) + np.mean(profit_C)
                if total_profit > sum(profits_at_nash):
                    best_quotas = quotas
                    profits_at_nash = [np.mean(profit_A), np.mean(profit_B), np.mean(profit_C)]
    
    return best_quotas, profits_at_nash
