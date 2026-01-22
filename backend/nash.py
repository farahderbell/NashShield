import numpy as np
from backend.simulation import simulation_3_assureurs, simulation_3_assureurs_different_claims


def nash_equilibrium_3_assureurs(S0, mu, sigma, T, N, quotas_options):
    """
    Trouve un équilibre de Nash approché pour 3 assureurs en testant différentes combinaisons de quotas.
    
    Approche : Pour chaque combinaison, vérifier que la somme des quotas ≤ 1,
    puis évaluer si c'est un candidat à l'équilibre en maximisant le bien-être social
    (somme des profits moyens).
    
    Args:
        S0, mu, sigma, T, N : paramètres GBM
        quotas_options : liste de quotas possibles pour chaque assureur (ex : [0.0, 0.05, 0.10, ...])
    
    Returns:
        best_quotas : liste des quotas au Nash equilibrium [qA, qB, qC]
        profits_at_nash : profits correspondants [profit_A, profit_B, profit_C]
    """
    
    best_quotas = [0.0, 0.0, 0.0]
    best_total_profit = float('-inf')
    profits_at_nash = [0.0, 0.0, 0.0]

    # Tester toutes les combinaisons valides de quotas
    for qA in quotas_options:
        for qB in quotas_options:
            for qC in quotas_options:
                # Respecter la contrainte : somme des quotas ≤ 1
                if qA + qB + qC > 1.0:
                    continue
                
                quotas = [qA, qB, qC]
                profit_A, profit_B, profit_C = simulation_3_assureurs(S0, mu, sigma, T, N, quotas)
                
                # Maximiser le bien-être social (somme des profits moyens)
                mean_A = np.mean(profit_A)
                mean_B = np.mean(profit_B)
                mean_C = np.mean(profit_C)
                total_profit = mean_A + mean_B + mean_C
                
                if total_profit > best_total_profit:
                    best_total_profit = total_profit
                    best_quotas = quotas
                    profits_at_nash = [mean_A, mean_B, mean_C]
    
    return best_quotas, profits_at_nash


def nash_equilibrium_3_assureurs_different_claims(S0A, S0B, S0C, mu, sigma, T, N, quotas_options):
    """
    Trouve un équilibre de Nash avec claims différents par assureur.
    
    Args:
        S0A, S0B, S0C : initial claims pour chaque assureur
        mu, sigma, T, N : paramètres GBM
        quotas_options : liste de quotas possibles
    
    Returns:
        best_quotas : liste des quotas au Nash equilibrium [qA, qB, qC]
        profits_at_nash : profits correspondants [profit_A, profit_B, profit_C]
    """
    
    best_quotas = [0.0, 0.0, 0.0]
    best_total_profit = float('-inf')
    profits_at_nash = [0.0, 0.0, 0.0]

    # Tester toutes les combinaisons valides de quotas
    for qA in quotas_options:
        for qB in quotas_options:
            for qC in quotas_options:
                # Respecter la contrainte : somme des quotas ≤ 1
                if qA + qB + qC > 1.0:
                    continue
                
                quotas = [qA, qB, qC]
                profit_A, profit_B, profit_C = simulation_3_assureurs_different_claims(
                    S0A, S0B, S0C, mu, sigma, T, N, quotas
                )
                
                # Maximiser le bien-être social (somme des profits moyens)
                mean_A = np.mean(profit_A)
                mean_B = np.mean(profit_B)
                mean_C = np.mean(profit_C)
                total_profit = mean_A + mean_B + mean_C
                
                if total_profit > best_total_profit:
                    best_total_profit = total_profit
                    best_quotas = quotas
                    profits_at_nash = [mean_A, mean_B, mean_C]
    
    return best_quotas, profits_at_nash
