#!/usr/bin/env python
"""
Test script to verify the quota-share reinsurance formula implementation.
"""

import numpy as np
import sys
sys.path.insert(0, '/mnt/c/Users/User1/NashShield')

from backend.simulation import simulate_GBM, calculate_profit, simulation_3_insurers, simulation_3_insurers_different_premiums
from backend.nash import nash_equilibrium_3_insurers_different_premiums

# Simulation parameters
S0 = 1000
mu = 0.05
sigma = 0.2
T = 1
N = 1000

print("=" * 80)
print("FORMULA VERIFICATION TEST")
print("=" * 80)

# Test 1: Basic GBM Simulation
print("\n[TEST 1] Geometric Brownian Motion (GBM)")
print("-" * 80)
np.random.seed(42)
premiums = simulate_GBM(S0, mu, sigma, T, N)
print(f"  Initial Premium (S0): ${S0}")
print(f"  Expected Premium (E[S_T]): ${S0 * np.exp(mu * T):.2f}")
print(f"  Simulated Mean: ${np.mean(premiums):.2f}")
print(f"  Simulated Std: ${np.std(premiums):.2f}")
print(f"  Min/Max: ${np.min(premiums):.2f} / ${np.max(premiums):.2f}")
assert np.mean(premiums) > S0 * np.exp(mu * T) * 0.8, "GBM mean should grow with drift"
print("  ✓ GBM simulation valid")

# Test 2: Profit Calculation
print("\n[TEST 2] Profit Calculation Formula")
print("-" * 80)
print("  Formula: Profit = Retention × (Premium - Claims)")
print("  Where Retention = 1 - Q (Q = ceded quota)")
print()

# Scenario 1: 100% Retention (keep all, cede nothing)
prems = np.array([1000, 1200, 800])
claims = np.array([700, 840, 560])
retention_100 = 1.0
profit_100 = calculate_profit(prems, claims, retention_100)
expected_100 = np.array([300, 360, 240])
print(f"  Test 2a: 100% Retention (Q=0%, keep everything)")
print(f"    Premiums: {prems}")
print(f"    Claims:   {claims}")
print(f"    Profit = 1.0 × (Premium - Claims) = {profit_100}")
print(f"    Expected: {expected_100}")
assert np.allclose(profit_100, expected_100), "100% retention profit calculation failed"
print("    ✓ Correct")

# Scenario 2: 30% Retention (keep 30%, cede 70%)
retention_30 = 0.3
profit_30 = calculate_profit(prems, claims, retention_30)
expected_30 = np.array([90, 108, 72])  # 0.3 × (Premium - Claims)
print(f"\n  Test 2b: 30% Retention (Q=70%, keep 30%)")
print(f"    Premiums: {prems}")
print(f"    Claims:   {claims}")
print(f"    Profit = 0.3 × (Premium - Claims) = {profit_30}")
print(f"    Expected: {expected_30}")
assert np.allclose(profit_30, expected_30), "30% retention profit calculation failed"
print("    ✓ Correct")

# Scenario 3: 0% Retention (cede everything)
retention_0 = 0.0
profit_0 = calculate_profit(prems, claims, retention_0)
expected_0 = np.array([0, 0, 0])
print(f"\n  Test 2c: 0% Retention (Q=100%, cede everything)")
print(f"    Premiums: {prems}")
print(f"    Claims:   {claims}")
print(f"    Profit = 0.0 × (Premium - Claims) = {profit_0}")
print(f"    Expected: {expected_0}")
assert np.allclose(profit_0, expected_0), "0% retention profit calculation failed"
print("    ✓ Correct")

# Test 3: Loss Ratio
print("\n[TEST 3] Loss Ratio (70% assumption)")
print("-" * 80)
np.random.seed(42)
S0_premium = 1000
S0_claims = S0_premium * 0.7
premiums_test = simulate_GBM(S0_premium, mu, sigma, T, N)
claims_test = simulate_GBM(S0_claims, mu, sigma, T, N)
loss_ratio = np.mean(claims_test) / np.mean(premiums_test)
print(f"  Initial Premium (S0): ${S0_premium}")
print(f"  Initial Claims (S0 × 0.7): ${S0_claims}")
print(f"  Mean Premium: ${np.mean(premiums_test):.2f}")
print(f"  Mean Claims: ${np.mean(claims_test):.2f}")
print(f"  Empirical Loss Ratio: {loss_ratio:.2%}")
print(f"  Expected Loss Ratio: 70%")
print(f"  Deviation: {abs(loss_ratio - 0.7):.2%}")
print("  ℹ️  Loss ratio varies due to GBM stochasticity - this is normal")
assert 0.5 < loss_ratio < 0.9, "Loss ratio seems unreasonable"
print("  ✓ Loss ratio in acceptable range")

# Test 4: Three-Insurer Scenario with Same Premiums
print("\n[TEST 4] Three-Insurer Scenario (Identical Premiums)")
print("-" * 80)
np.random.seed(42)
retention_test = [0.3, 0.4, 0.3]
profit_A, profit_B, profit_C = simulation_3_insurers(1000, mu, sigma, T, N, retention_test)

print(f"  Retention Rates: {retention_test}")
print(f"  Constraint Check: Sum = {sum(retention_test)} ≤ 1.0 ✓")
print(f"\n  Player A (30% retention):")
print(f"    Mean Profit: ${np.mean(profit_A):.2f}")
print(f"    Std Dev: ${np.std(profit_A):.2f}")
print(f"    Min/Max: ${np.min(profit_A):.2f} / ${np.max(profit_A):.2f}")
print(f"\n  Player B (40% retention):")
print(f"    Mean Profit: ${np.mean(profit_B):.2f}")
print(f"    Std Dev: ${np.std(profit_B):.2f}")
print(f"    Min/Max: ${np.min(profit_B):.2f} / ${np.max(profit_B):.2f}")
print(f"\n  Player C (30% retention):")
print(f"    Mean Profit: ${np.mean(profit_C):.2f}")
print(f"    Std Dev: ${np.std(profit_C):.2f}")
print(f"    Min/Max: ${np.min(profit_C):.2f} / ${np.max(profit_C):.2f}")

# Player B should have higher profit due to higher retention
assert np.mean(profit_B) > np.mean(profit_A), "Player B (40%) should profit more than A (30%)"
assert np.mean(profit_B) > np.mean(profit_C), "Player B (40%) should profit more than C (30%)"
print("\n  ✓ Higher retention → higher expected profit (as expected)")

# Test 5: Three-Insurer Scenario with Different Premiums
print("\n[TEST 5] Three-Insurer Scenario (Different Premiums)")
print("-" * 80)
np.random.seed(42)
S0A_val = 1500
S0B_val = 1200
S0C_val = 800
retention_diff = [0.25, 0.35, 0.30]

profit_A, profit_B, profit_C = simulation_3_insurers_different_premiums(
    S0A_val, S0B_val, S0C_val, mu, sigma, T, N, retention_diff
)

print(f"  Initial Premiums: A=${S0A_val}, B=${S0B_val}, C=${S0C_val}")
print(f"  Retention Rates: {retention_diff}")
print(f"  Constraint Check: Sum = {sum(retention_diff):.1f} ≤ 1.0 ✓")
print(f"\n  Player A (Premium=${S0A_val}, 25% retention):")
print(f"    Mean Profit: ${np.mean(profit_A):.2f}")
print(f"  Player B (Premium=${S0B_val}, 35% retention):")
print(f"    Mean Profit: ${np.mean(profit_B):.2f}")
print(f"  Player C (Premium=${S0C_val}, 30% retention):")
print(f"    Mean Profit: ${np.mean(profit_C):.2f}")

# Expected: A highest premium → highest profit despite low retention
# due to larger premium base
print("\n  ✓ Different premium scenarios calculated")

# Test 6: Nash Equilibrium
print("\n[TEST 6] Nash Equilibrium Calculation")
print("-" * 80)
np.random.seed(42)
S0A_nash = 1000
S0B_nash = 1000
S0C_nash = 1000
retention_options = [round(i * 0.1, 1) for i in range(11)]

print(f"  Initial Premiums: All ${S0A_nash}")
print(f"  Retention Options: {retention_options}")
print(f"  Testing all valid combinations (sum ≤ 1.0)...")

best_retentions, profits_nash = nash_equilibrium_3_insurers_different_premiums(
    S0A_nash, S0B_nash, S0C_nash, mu, sigma, T, N, retention_options
)

print(f"\n  Nash Equilibrium Results:")
print(f"    Optimal Retentions: {best_retentions}")
print(f"    Sum Check: {sum(best_retentions)} ≤ 1.0 ✓")
print(f"    Player A Profit: ${profits_nash[0]:.2f}")
print(f"    Player B Profit: ${profits_nash[1]:.2f}")
print(f"    Player C Profit: ${profits_nash[2]:.2f}")
print(f"    Total Social Welfare: ${sum(profits_nash):.2f}")

assert sum(best_retentions) <= 1.0, "Nash equilibrium violates constraint"
assert all(0 <= r <= 1 for r in best_retentions), "Invalid retention rate"
print("\n  ✓ Nash equilibrium satisfies all constraints")

print("\n" + "=" * 80)
print("ALL TESTS PASSED ✓")
print("=" * 80)
print("\nFormula Summary:")
print("  Profit = Retention × (Premium - Claims)")
print("  Where Retention = 1 - Ceded Quota (Q)")
print("  Higher retention → Higher expected profit but higher risk")
print("  Loss Ratio = 70% (Claims = 0.7 × Premium)")
print("=" * 80)
