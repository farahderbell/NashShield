# 📊 Real Quota-Share Reinsurance - Mathematical Reference

## Complete Formula Reference

---

## 1. Core Quota-Share Formulas

### Terminology Relationships
```
Q = Quota Cédée (percentage CEDED to reinsurer)
Retention = 1 - Q (percentage KEPT by primary insurer)

Constraint: 0 ≤ Q ≤ 1
Constraint: 0 ≤ Retention ≤ 1
Relationship: Retention + Q = 1.0
```

### Premium Split (Revenue Sharing)
```
Primary Insurer's Premium:
  Primary_Premium = (1 - Q) × Total_Premium
                  = Retention × Total_Premium

Reinsurer's Premium:
  Ceded_Premium = Q × Total_Premium
```

### Claims Split (Loss Sharing)
```
Primary Insurer's Claims:
  Primary_Claims = (1 - Q) × Total_Claims
                 = Retention × Total_Claims

Reinsurer's Claims:
  Ceded_Claims = Q × Total_Claims
```

### Profit Calculation
```
Net Income = Total_Premium - Total_Claims

Primary Insurer's Profit:
  Profit = (1 - Q) × (Total_Premium - Total_Claims)
         = Retention × (Premium - Claims)
         = Primary_Premium - Primary_Claims
```

---

## 2. Geometric Brownian Motion (GBM)

### Formula
$$S_T = S_0 \cdot e^{(\mu - \frac{\sigma^2}{2})T + \sigma\sqrt{T}Z}$$

Where:
- $S_0$ = Initial value (premium or claim base)
- $\mu$ = Drift (mean growth rate) = 0.05 per year
- $\sigma$ = Volatility (standard deviation) = 0.20 per year
- $T$ = Time horizon = 1 year
- $Z$ = Standard normal random variable ~ N(0,1)
- $S_T$ = Value at time T

### Parameters Used in NashShield
```
μ (drift) = 0.05         (5% expected annual growth)
σ (sigma) = 0.20         (20% standard deviation)
T (time) = 1             (1 year horizon)
N = 1000                 (1000 Monte Carlo simulations)
```

### Premium Simulation
```
Premium_T = Premium_0 × exp((μ - σ²/2)T + σ√T × Z)
          = Premium_0 × exp((0.05 - 0.02)×1 + 0.2√1 × Z)
          = Premium_0 × exp(0.03 + 0.2Z)
```

### Claims Simulation (70% Loss Ratio)
```
Claims_T = Claims_0 × exp((μ - σ²/2)T + σ√T × Z)

Where: Claims_0 = 0.7 × Premium_0
       (Realistic assumption: claims average 70% of premiums)

Claims_T = 0.7×Premium_0 × exp(0.03 + 0.2Z)
```

---

## 3. Profit Calculation Pipeline

### Step 1: Generate Random Scenarios
```
For each simulation i = 1 to 1000:
  Z_i ~ N(0, 1)
  
  Premium_i = S0 × exp(0.03 + 0.2×Z_i)
  Claims_i = 0.7×S0 × exp(0.03 + 0.2×Z_i)
```

### Step 2: Calculate Individual Insurer Profit
```
For insurer with retention rate Ret:
  Profit_i = Ret × (Premium_i - Claims_i)
           = Ret × [S0×exp(...) - 0.7×S0×exp(...)]
           = Ret × S0 × exp(...) × (1 - 0.7)
           = Ret × S0 × 0.3 × exp(...)
```

### Step 3: Average Across Simulations
```
Average_Profit = (1/1000) × Σ(Profit_i) for i=1 to 1000
```

---

## 4. Concrete Example

### Setup
```
Insurer A:
  S0A = $1,000 (initial premium)
  Ret_A = 0.30 (keeps 30%, cedes 70%)
```

### Scenario Simulation (Single Path)
```
Z = 1.5 (random normal variable)

Premium_1 = $1,000 × exp(0.03 + 0.2×1.5)
          = $1,000 × exp(0.03 + 0.30)
          = $1,000 × exp(0.33)
          = $1,000 × 1.391
          = $1,391

Claims_1 = $700 × exp(0.33)
         = $700 × 1.391
         = $973.70

Profit_1 = 0.30 × ($1,391 - $973.70)
         = 0.30 × $417.30
         = $125.19
```

### Revenue/Claims Split (Same Scenario)
```
Total Revenue: $1,391
  Insurer A keeps: 30% = $417.30
  Reinsurer gets: 70% = $972.70

Total Claims: $973.70
  Insurer A pays: 30% = $292.11
  Reinsurer pays: 70% = $681.59

Insurer A Net Profit:
  Revenue_in - Claims_out = $417.30 - $292.11 = $125.19 ✓
```

---

## 5. Multi-Insurer Nash Equilibrium

### Setup (3 Insurers)
```
Parameters: S0A = S0B = S0C = $1,000
Retention Options: [0.0, 0.1, 0.2, ..., 0.5, ..., 1.0]

Constraint: Ret_A + Ret_B + Ret_C ≤ 1.0
```

### Objective Function
```
Maximize: Total_Profit = Profit_A + Profit_B + Profit_C

Where:
  Profit_A = Ret_A × (Premium_A - Claims_A)
  Profit_B = Ret_B × (Premium_B - Claims_B)
  Profit_C = Ret_C × (Premium_C - Claims_C)
```

### Example Optimal Solution
```
Testing: (0.3, 0.3, 0.3)
  Total_Profit = 0.3×300 + 0.3×300 + 0.3×300 = 270 (avg across 1000 sims)
  Constraint: 0.3 + 0.3 + 0.3 = 0.9 ≤ 1.0 ✓

Testing: (0.4, 0.3, 0.2)
  Total_Profit = 0.4×300 + 0.3×300 + 0.2×300 = 270 (similar)
  Constraint: 0.4 + 0.3 + 0.2 = 0.9 ≤ 1.0 ✓

Testing: (0.5, 0.5, 0.5)
  Constraint: 0.5 + 0.5 + 0.5 = 1.5 > 1.0 ✗ (INVALID - skipped)

Nash Equilibrium Result: (0.3, 0.3, 0.3) or similar high-profit combo
```

---

## 6. Comparison: Before vs After

### OLD MODEL (Simplified)
```
Profit = (1 - q) × Claims

Problems:
  - Only considers claims, ignores premiums
  - Not realistic for insurance business
  - Doesn't match real quota-share contracts
  - Missing revenue component

Example:
  Claims = $200
  q = 0.3 (30% quota)
  Profit = 0.7 × $200 = $140
  
  Issue: Doesn't account for premiums collected!
```

### NEW MODEL (Real)
```
Profit = Retention × (Premium - Claims)
       = (1 - Q) × (Premium - Claims)

Advantages:
  - Considers both revenue (premiums) and costs (claims)
  - Matches real insurance profit calculation
  - Aligns with actual quota-share reinsurance formulas
  - Realistic financial modeling

Example:
  Premium = $1,000
  Claims = $200
  Retention = 0.3 (keep 30%, cede 70%)
  Profit = 0.3 × ($1,000 - $200)
         = 0.3 × $800
         = $240
```

---

## 7. Statistical Properties

### GBM Distribution
```
log(S_T / S_0) ~ Normal(μT - σ²T/2, σ²T)

For our parameters:
  μT - σ²T/2 = 0.05×1 - 0.04×1/2 = 0.05 - 0.02 = 0.03
  σ²T = 0.04×1 = 0.04
  
  log(S_T / S_0) ~ Normal(0.03, 0.04)
  
Mean S_T / S_0 = exp(0.03 + 0.04/2) = exp(0.05) ≈ 1.051

So premiums/claims grow by ~5.1% on average
```

### Profit Distribution
```
Due to randomness, each simulation yields different profit:
  Profit_min (worst case) = Low profit scenario
  Profit_mean (expected) = Average across 1000 sims
  Profit_max (best case) = High profit scenario
  
Display: Profit_mean (what user sees as "expected profit")
```

---

## 8. Constraint Validation

### Valid Retention Combinations
```
Ret_A = 0.3, Ret_B = 0.3, Ret_C = 0.3
Sum = 0.9 ≤ 1.0 ✓ VALID

Ret_A = 0.5, Ret_B = 0.5, Ret_C = 0.1
Sum = 1.1 > 1.0 ✗ INVALID (skipped by Nash solver)
```

### Why Constraint Matters
```
If sum of retentions > 1.0:
  Remaining risk = 1 - (Ret_A + Ret_B + Ret_C) < 0
  Negative risk = impossible!
  
This would mean reinsurers must pay MORE than total claims.
Mathematically and actuarially invalid.
```

---

## 9. Implementation in Code

### Python Formula
```python
def calculer_profit(primes, sinistres, retention):
    """
    Real Quota-Share Formula Implementation
    
    profit = retention × (primes - sinistres)
    
    Args:
        primes: Array of premium amounts from GBM
        sinistres: Array of claim amounts from GBM
        retention: Insurer's retention rate (0-1)
    
    Returns:
        profit: Array of profit amounts
    """
    profit = retention * (primes - sinistres)
    return profit
```

### Usage Example
```python
# Generate scenarios
primes = simulate_GBM(S0=1000, mu=0.05, sigma=0.2, T=1, N=1000)
sinistres = simulate_GBM(S0=700, mu=0.05, sigma=0.2, T=1, N=1000)

# Calculate profit with 30% retention
retention = 0.30
profit = calculer_profit(primes, sinistres, retention)

# Get expected value
expected_profit = np.mean(profit)
```

---

## 10. Real-World Quota-Share Examples

### Example 1: QP70%
```
Q = 70% (quota cédée)
Retention = 30%

Interpretation: Primary insurer keeps 30% of revenue/losses
               Reinsurer takes 70% of revenue/losses
```

### Example 2: QP50%
```
Q = 50% (quota cédée)
Retention = 50%

Interpretation: 50-50 split between insurer and reinsurer
```

### Example 3: QP90%
```
Q = 90% (quota cédée)
Retention = 10%

Interpretation: Primary insurer keeps only 10%
               Reinsurer handles 90% (high-risk transfer)
```

---

## Summary Table

| Concept | Formula | Meaning |
|---------|---------|---------|
| **Ceded Quota** | Q | % transferred to reinsurer |
| **Retention** | 1 - Q | % kept by primary insurer |
| **Ceded Premium** | Q × Premium | Premium to reinsurer |
| **Retained Premium** | (1-Q) × Premium | Premium kept by insurer |
| **Ceded Claims** | Q × Claims | Claims paid by reinsurer |
| **Retained Claims** | (1-Q) × Claims | Claims paid by insurer |
| **Insurer Profit** | (1-Q) × (P - S) | Net profit = revenue - costs |
| **Premium Path** | GBM(S₀, μ, σ, T, Z) | Stochastic premium evolution |
| **Claims Path** | GBM(0.7×S₀, μ, σ, T, Z) | Stochastic claims with 70% ratio |

---

**This document provides complete mathematical foundation for NashShield's real quota-share formula implementation.**
