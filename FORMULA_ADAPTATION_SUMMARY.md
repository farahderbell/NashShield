# 🛡️ Real Quota-Share Formula Adaptation - COMPLETE

## Summary of Changes

The entire NashShield project has been successfully adapted to use the **REAL insurance quota-share formula** instead of simplified models.

---

## 1. ✅ Backend Simulation (`backend/simulation.py`)

### Changes Made:
- **Replaced** simplified profit formula: `profit = (1 - q) × claims`
- **With real formula**: `profit = retention × (primes - sinistres)`
- **Added** separate GBM simulation for **Primes** (insurance premiums collected)
- **Added** separate GBM simulation for **Sinistres** (insurance claims paid out)
- **Realistic assumption**: Sinistres = GBM(S₀ × 0.7) = 70% loss ratio

### Key Functions:
```python
def calculer_profit(primes, sinistres, retention):
    """
    Real Formula: Profit = Retention × (Primes - Sinistres)
    Where:
    - Retention = 1 - Q (percent kept by insurer)
    - Q = Quota cédée (percent ceded to reinsurer)
    - Primes = Insurance premiums collected
    - Sinistres = Insurance claims paid
    """
    profit = retention * (primes - sinistres)
    return profit
```

### Formula Documentation:
```
QP70% Example (70% ceded quota):
- Ceded Quota Q = 70%
- Retention = 30% = (1 - Q)
- Prime cédée = Q × Pi = 0.7 × Premium
- Charge cédée = Q × Si = 0.7 × Claims
- Profit = Retention × (Premium - Claims) = 0.3 × (P - S)
```

---

## 2. ✅ Nash Equilibrium Solver (`backend/nash.py`)

### Changes Made:
- **Renamed variables**: `quotas` → `retentions` for clarity
- **Updated documentation**: References real quota-share formula
- **Constraint validation**: Sum of retentions ≤ 1.0
- **Optimization**: Maximizes total profit using real formula

### Key Functions:
```python
def nash_equilibrium_3_assureurs_different_claims(S0A, S0B, S0C, mu, sigma, T, N, retention_options):
    """
    Finds optimal retention rates using real quota-share formula
    """
    # Tests all valid combinations
    # Constraint: sum of retentions ≤ 1.0
    # Maximizes: total expected profit
```

---

## 3. ✅ Flask API Backend (`backend/app.py`)

### Changes Made:
- **Parameter docs**: Added comprehensive docstring explaining real formula
- **Variable naming**: Updated for clarity (retention terminology)
- **API endpoint**: `/simulate` now clearly documents the real formula
- **Constraint validation**: Validates sum of retentions ≤ 1.0

### API Documentation:
```python
"""
Real Formula:
- Q = Ceded quota percentage (e.g., 0.7 = 70% ceded)
- Retention = 1 - Q (percentage kept by primary insurer)
- Prime cédée = Q × Prime (ceded premium)
- Charge cédée = Q × Sinistre (ceded claim)
- Profit = Retention × (Prime - Sinistre)
"""
```

---

## 4. ✅ Frontend HTML (`templates/index.html`)

### Changes Made:
- **Terminology**: "Quota" → "Retention Rate"
- **Section Title**: "💰 Initial Claims" → "💰 Initial Premiums by Insurer"
- **Slider Labels**: Updated to reflect retention concept
- **How It Works**: Complete rewrite showing real formula with:
  - Q = Quota cédée (percent ceded)
  - Retention = 1 - Q (percent kept)
  - Prime cédée = Q × Pi formula
  - Charge cédée = Q × Si formula
  - Real profit formula: Retention × (Prime - Sinistre)
- **Hints**: Updated to explain retention vs ceded distinction
- **Scenario description**: Updated for Nash equilibrium concept

### Key HTML Sections Updated:
```html
<!-- How It Works Card -->
"Real Quota-Share Reinsurance Formula:"
- Q = Quota cédée (percentage ceded to reinsurer) → e.g., 70%
- Retention = 1 - Q (percentage kept by primary insurer) → e.g., 30%
- Prime cédée = Q × Prime (ceded premium to reinsurer)
- Charge cédée = Q × Sinistre (ceded claims to reinsurer)
- Profit Formula: Profit = Retention × (Prime - Sinistre)

<!-- Initial Premiums Section -->
Sliders renamed from "Claims" to "Premiums"
Descriptions updated to show premium-based calculations

<!-- Player Retention Strategies -->
Section title changed to "Players' Retention Strategies"
Slider labels show "Retention Rate"
Hints explain: 0 = cede all risk, 1 = retain all risk
```

---

## 5. ✅ Documentation (`README.md`)

### Changes Made:
- **Section "How It Works"**: Complete rewrite for real formula
  - Shows 5-step premium/claim process
  - Real quota-share terminology
  - Visual relationship between Q and Retention
- **Mathematical Foundation**: New section added!
  - Complete real quota-share formula with QP70% example
  - Step-by-step profit calculation example
  - Shows Premium split, Claims split, and final profit
- **Core Concepts**: Updated "Quota-Share Reinsurance"
  - Real insurance example with actual numbers
  - Shows premium split, claims split, final profit calculation
  - Explains QP70% = 30% retention
- **Example Calculation**:
  ```
  QP70% Quota-Share Example:
  - Q = 70% (ceded to reinsurer)
  - Retention = 30% (kept by primary insurer)
  - Prime collected = $1,000
  - Prime cédée = 70% × $1,000 = $700
  - Claims paid = $200
  - Charge cédée = 70% × $200 = $140
  - Profit = 30% × ($1,000 - $200) = $240
  ```

---

## 6. Mathematical Formulas (All Updated)

### Real Quota-Share Formula:
$$\text{Prime cédée} = Q \times P_i$$
$$\text{Charge cédée} = Q \times S_i$$
$$\text{Profit} = (1-Q) \times (P_i - S_i) = \text{Retention} \times (\text{Prime} - \text{Sinistre})$$

### GBM Simulation (For both Primes and Sinistres):
$$S_T = S_0 \cdot e^{(\mu - \frac{\sigma^2}{2})T + \sigma\sqrt{T}Z}$$

### Nash Equilibrium (With Retention Constraint):
$$\text{NE} = \arg\max_{\text{Ret}_A, \text{Ret}_B, \text{Ret}_C} \left[ \mathbb{E}[\text{Profit}_A] + \mathbb{E}[\text{Profit}_B] + \mathbb{E}[\text{Profit}_C] \right]$$
Subject to: $\text{Ret}_A + \text{Ret}_B + \text{Ret}_C \leq 1$

---

## 7. Parameter Definitions

| Parameter | Symbol | Meaning | Example |
|-----------|--------|---------|---------|
| Ceded Quota | Q | % ceded to reinsurer | 70% |
| Retention | 1-Q | % kept by insurer | 30% |
| Prime | Pi | Total insurance premium | $1,000 |
| Prime cédée | Q×Pi | Premium to reinsurer | $700 |
| Sinistre | Si | Total insurance claims | $200 |
| Charge cédée | Q×Si | Claims to reinsurer | $140 |
| Profit | (1-Q)×(Pi-Si) | Insurer's net profit | $240 |

---

## 8. Constraint Validation

**Original Constraint**: Sum of quotas ≤ 1.0
**Real Constraint**: Sum of retention rates ≤ 1.0

Both enforce the same mathematical principle: total risk coverage must not exceed 100%.

**Why?** If retention rates sum to > 1.0, reinsurers would need to cover more than 100% of risks, which is mathematically impossible.

---

## 9. Simulation Parameters (Unchanged)

```
GBM Parameters:
- μ (drift) = 0.05 = 5% annual growth
- σ (volatility) = 0.2 = 20% standard deviation
- T (time horizon) = 1 year
- N (simulations) = 1,000 Monte Carlo runs

Loss Ratio:
- Sinistres = GBM(S₀ × 0.7, ...) = 70% realistic ratio
```

---

## 10. Files Modified Summary

| File | Changes | Status |
|------|---------|--------|
| `backend/simulation.py` | Real formula, GBM for primes+sinistres | ✅ Done |
| `backend/nash.py` | Retention terminology, constraint validation | ✅ Done |
| `backend/app.py` | API docs, retention terminology, constraint validation | ✅ Done |
| `templates/index.html` | Terminology, formulas, UI updates | ✅ Done |
| `README.md` | Complete real formula documentation | ✅ Done |

---

## 11. How to Use the Updated System

### Classic Scenario:
1. Set **Initial Premiums** for each insurer (S₀A, S₀B, S₀C)
2. Set **Retention Rates** for each (0 = cede all, 1 = keep all)
3. Click "Run Simulation"
4. See profits calculated using: **Profit = Retention × (Premium - Claims)**

### Nash Equilibrium Scenario:
1. Set **Initial Premiums** for each insurer
2. System automatically finds optimal **Retention Rates**
3. Click "Run Simulation"
4. See optimal profits where no insurer can improve alone

---

## 12. Key Improvements Over Previous Version

| Aspect | Before | After |
|--------|--------|-------|
| **Formula** | Simplified: (1-q)×claims | Real: retention×(primes-sinistres) |
| **Primes** | Not modeled | GBM simulated separately |
| **Sinistres** | Simplified claims | GBM with 70% loss ratio |
| **Terminology** | "Quota" ambiguous | Clear: Q (ceded), Retention (kept) |
| **Accuracy** | Educational only | Realistic insurance model |
| **Documentation** | Basic | Comprehensive with real formulas |

---

## 13. Verification

✅ **Code Syntax**: All Python files updated and syntactically correct
✅ **Formula Implementation**: Real quota-share formula implemented in simulation
✅ **API**: Flask endpoints updated with new parameter handling
✅ **Frontend**: HTML terminology and formulas updated
✅ **Documentation**: README fully updated with real formulas
✅ **Constraint Validation**: Sum of retentions ≤ 1.0 enforced

---

## 14. Next Steps (Optional)

To further enhance accuracy:
1. Add **loading costs** (operational expenses as % of premium)
2. Add **commission rates** (broker/agent fees)
3. Add **reinsurer profit margin**
4. Implement **catastrophe bonds** (extreme loss scenarios)
5. Add **risk adjusted returns** (Sharpe ratio optimization)

---

**Status**: ✅ **COMPLETE**

The entire NashShield project now uses the real insurance quota-share formula with proper premium and claim modeling. All components have been updated consistently and tested for compatibility.

**Ready for**: Educational use demonstrating real quota-share reinsurance mechanics
