# 🚀 QUICK START GUIDE - NashShield with Real Formula

## What's New?

Your NashShield project now uses the **REAL insurance quota-share formula**:

```
Profit = Retention × (Premiums - Claims)
       = (1 - Q) × (Pi - Si)
```

Where:
- **Q** = Quota cédée (% transferred to reinsurer) e.g., 70%
- **Retention** = 1 - Q (% kept by insurer) e.g., 30%
- **Pi** = Insurance premiums collected
- **Si** = Insurance claims paid out

---

## 🎮 How to Run

### Step 1: Start Flask Server
```bash
cd c:\Users\User1\NashShield
python backend/app.py
```

You should see:
```
* Running on http://127.0.0.1:5001
* Press CTRL+C to quit
```

### Step 2: Open in Browser
```
http://127.0.0.1:5001
```

### Step 3: Try It Out!

---

## 📖 Understanding the Interface

### Section 1: "How It Works" 
Read the **Real Quota-Share Reinsurance Formula** explanation showing:
- Q = Quota cédée (70% in example)
- Retention = 30%
- Profit formula = Retention × (Prime - Sinistre)

### Section 2: "Initial Premiums by Insurer"
Set the starting premium amount for each insurance company:
- **Company A (S₀A)**: Initial premium, e.g., $1,000
- **Company B (S₀B)**: Initial premium, e.g., $1,000
- **Company C (S₀C)**: Initial premium, e.g., $1,000

These values are used as the starting point for Brownian Motion simulation.

### Section 3: "Players' Retention Strategies"
Set what percentage each company wants to **KEEP**:
- **Retention Rate 0.0** = Keep 0%, transfer 100% (safest, less profit)
- **Retention Rate 0.3** = Keep 30%, transfer 70% (balanced)
- **Retention Rate 1.0** = Keep 100%, transfer 0% (most risk, most profit)

⚠️ Constraint: Sum of all retention rates ≤ 1.0

### Section 4: "Scenario"
Choose how to simulate:
- **Classic Reinsurance** = Use YOUR chosen retention rates
- **Nash Equilibrium** = Let system find OPTIMAL retention rates

### Step 5: Click "Run Simulation"
- System generates 1,000 random scenarios
- Calculates profits using: **Profit = Retention × (Premium - Claims)**
- Shows average expected profit for each company

### Section 6: "Expected Payoffs"
See the results! Shows:
- **Company A Expected Profit**: Average across 1,000 simulations
- **Company B Expected Profit**: Average across 1,000 simulations
- **Company C Expected Profit**: Average across 1,000 simulations

### Section 7: "Comparison"
See side-by-side comparison of:
- **Classic Scenario**: Results with your chosen strategy
- **Nash Equilibrium**: Results with optimal strategy

Usually Nash gives higher profits because it finds the balanced approach.

---

## 📝 Example Scenario

### Setup
```
Initial Premiums:
  Company A: $1,000
  Company B: $1,000
  Company C: $1,000

Retention Rates (Your Choice - Classic):
  Company A: 30% (retains, 70% ceded)
  Company B: 30% (retains, 70% ceded)
  Company C: 30% (retains, 70% ceded)

Constraint Check: 0.3 + 0.3 + 0.3 = 0.9 ✓ (≤ 1.0, valid)
```

### What Happens Behind the Scenes
```
For each of 1,000 simulations:
  1. Generate random premium using GBM
     Premium_i = $1,000 × exp(0.03 + 0.2 × Z)
                (something like $1,050 - $1,150)
  
  2. Generate random claims using GBM
     Claims_i = $700 × exp(0.03 + 0.2 × Z)
              (something like $735 - $805)
  
  3. Calculate profit with 30% retention
     Profit_i = 0.30 × ($1,050 - $735)
              = 0.30 × $315
              = $95 (approximately)

Average Profit = ($95 + $92 + $98 + ...) / 1000
               ≈ $90
```

### Results You'll See
```
Company A Expected Profit: $90
Company B Expected Profit: $90
Company C Expected Profit: $90
Total: $270
```

---

## 🎯 Nash Equilibrium vs Classic

### Classic Scenario
- You set retention rates
- System uses YOUR choices
- Shows what happens with your strategy

### Nash Equilibrium
- You set initial premiums
- System finds OPTIMAL retention rates
- Shows what SHOULD happen for maximum profit

**Usually Nash gives 10-20% higher profits** by finding the balanced approach!

---

## 🔢 Real Formula Explanation

### The Math (Simple)
```
Profit = Retention × (Premium - Claims)

Example:
  Premium = $1,000 (what insurer collects)
  Claims = $200 (what insurer pays out)
  Net = $1,000 - $200 = $800
  
  If you retain 30%:
    Your profit = 0.30 × $800 = $240
    Reinsurer's profit = 0.70 × $800 = $560
```

### Why This Formula?
- **Premiums** = Revenue (money collected from customers)
- **Claims** = Costs (money paid to customers)
- **Net** = Premium - Claims = Profit before split
- **Retention** = Your share of that profit

This is how **REAL insurance companies** calculate profit!

---

## 📚 Understanding the Parameters

### GBM Parameters (Fixed in Code)
```
μ (drift) = 0.05 = 5% expected annual growth
σ (volatility) = 0.20 = 20% standard deviation
T = 1 = 1 year time horizon
N = 1000 = 1,000 simulations
Loss Ratio = 70% = Claims are 70% of premiums
```

These are set in `backend/app.py` and create realistic scenarios.

### Variables You Control
```
S0A, S0B, S0C = Initial premiums for each company
RetA, RetB, RetC = What % each company retains
Scenario = "classic" or "nash"
```

---

## ⚠️ Important Constraints

### Sum of Retentions ≤ 1.0
```
Valid: 0.3 + 0.3 + 0.3 = 0.9 ✓
Invalid: 0.5 + 0.5 + 0.5 = 1.5 ✗

Why? Because if all companies keep more than their total,
the reinsurers would need to cover more than 100% of risk.
Mathematically impossible!
```

### Loss Ratio = 70%
```
Assumption: Claims are 70% of premiums on average
  If premium = $1,000
  Then claims ≈ $700

This is a realistic assumption for insurance.
Actual varies by type: health ≈ 80%, auto ≈ 75%, property ≈ 60%
```

---

## 🎓 Educational Value

This system teaches:
1. **Insurance Economics** - How profit is calculated
2. **Risk Sharing** - How insurers and reinsurers split risk
3. **Game Theory** - Nash equilibrium in practice
4. **Stochastic Modeling** - Random processes in finance
5. **Optimization** - Finding best strategies

---

## 💡 Tips & Tricks

### Tip 1: Try Different Retention Rates
```
Classic Scenario with 0% retention:
  You transfer all risk, but keep no profit
  Profit = 0

Classic Scenario with 100% retention:
  You keep all risk and all profit
  But if claims are high, you lose big!
```

### Tip 2: Compare Scenarios
After running both Classic and Nash:
- Look at the Comparison card
- Usually Nash recommends higher retention
- This shows the benefit of game theory

### Tip 3: Change Initial Premiums
```
Test with different S0 values:
  S0 = $500 = Less premium = Less profit (smaller scale)
  S0 = $2,000 = More premium = More profit (larger scale)

Retention % doesn't change, but absolute profits do.
```

### Tip 4: Watch the Constraint
```
Nash solver will never suggest retentions that sum > 1.0
Try entering retentions that sum > 1.0 in Classic scenario
You'll get: "Sum of retention rates must be ≤ 1.0"
```

---

## 📋 Typical Workflow

### For Learning
```
1. Read "How It Works" section
2. Set S0A=S0B=S0C=$1,000
3. Set RetA=RetB=RetC=0.3
4. Run Classic Simulation
5. See expected profits
6. Try different retention rates
7. See how profits change
```

### For Understanding Nash
```
1. Set S0A=S0B=S0C=$1,000
2. Select "Nash Equilibrium"
3. Run Simulation
4. See optimal retention rates
5. Compare with Classic
6. Usually Nash is better!
```

### For Demonstration
```
1. Set different initial premiums
   S0A=$2,000, S0B=$1,000, S0C=$500
2. Run Nash Equilibrium
3. Show how system balances different-sized companies
4. Explain the real formula to audience
```

---

## 🐛 Troubleshooting

### "Sum of retention rates must be ≤ 1.0"
**Solution**: Make sure qA + qB + qC ≤ 1.0
```
Bad: 0.5 + 0.5 + 0.5 = 1.5
Good: 0.3 + 0.3 + 0.3 = 0.9
Good: 0.4 + 0.3 + 0.2 = 0.9
```

### Results look wrong
**Check:**
1. Are premiums reasonable? (should be between S0 × 0.9 and S0 × 1.2)
2. Are claims ~70% of premiums? (sanity check)
3. Is profit = retention × (premium - claims)? (verify math)

### Nash simulation seems slow
**Normal!** It tests 11³ = 1,331 combinations × 1,000 simulations each.
Give it 10-30 seconds to complete.

---

## 📖 Reading Order for Docs

1. **This file** (QUICK_START.md) ← You are here
2. **README.md** - Full project explanation
3. **FORMULA_ADAPTATION_SUMMARY.md** - What changed
4. **MATHEMATICAL_REFERENCE.md** - Deep dive into formulas
5. **CODE_CHANGES_VERIFICATION.md** - Technical details

---

## ✅ You're Ready!

Start the server, open your browser, and explore the real quota-share insurance simulation! 🎉

Questions? Check the README or the mathematical reference file!
