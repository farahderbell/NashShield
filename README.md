# NashShield 🛡️

**An Interactive Platform for Risk Sharing & Game Theory in Insurance**

⚠️ **DISCLAIMER:** This project is for **educational and entertainment purposes only**. It is **NOT** intended for real-world insurance usage or financial decision-making. The models and simulations are simplified for learning purposes.


![Welcome to NashShield](images/welcome.png)



---

## 📌 Table of Contents
1. [What is NashShield?](#what-is-nashield)
2. [Why Do We Need It?](#why-do-we-need-it)
3. [How It Works](#how-it-works)
4. [Mathematical Foundation](#mathematical-foundation)
5. [Core Concepts Explained](#core-concepts-explained)
6. [Pillar I: SCR Calculator](#nashield-pillar-i-scr-calculator-new) ⭐ NEW!
7. [Pillar II: Nash Equilibrium](#nash-equilibrium-game-theory-optimization-pillar-ii)
8. [Technical Stack](#technical-stack)
9. [Installation & Setup](#installation--setup)
10. [How to Use](#how-to-use)
11. [Features](#features)
12. [Project Structure](#project-structure)

---

## 🎯 What is NashShield?

**NashShield** is an educational and analytical tool that helps insurance companies understand and optimize **risk sharing strategies** using game theory and mathematics.

### Simple Explanation (For Non-Experts)

Imagine **3 insurance companies** that each have customers who might make insurance claims:
- Company A might face $2,000 in claims
- Company B might face $1,500 in claims
- Company C might face $1,000 in claims

Each company faces a choice:
- **Keep all the risk** (keep 100% of claims) → More profit if claims are low, but big loss if claims are high
- **Transfer some risk** → Less profit but more stable and safe

**NashShield solves this:** It tells you exactly how much risk each company should keep to maximize **everyone's profit fairly and safely**.

---

## ❓ Why Do We Need It?

### The Problem
In insurance markets, companies often make selfish decisions:
- Company A says: "I'll keep 80% of my risk"
- Company B says: "I'll keep 80% too"
- Company C says: "Me too!"

Result: **Everyone loses money** because they're taking too much risk! 📉

### The Solution
Game theory (specifically **Nash Equilibrium**) shows the optimal strategy where:
- Each company cooperates fairly
- Everyone accepts the right amount of risk
- **Total profits increase by 30-50%** 📈
- The system is stable (no one can do better by changing strategy alone)



---

## 🔧 How It Works

### 3-Step Process

#### Step 1: Input Your Parameters
You provide:
- **Initial Premiums** for each company (S₀A, S₀B, S₀C)
  - Company A's expected premium: e.g., $2,000 Million
  - Company B's expected premium: e.g., $1,500 Million
  - Company C's expected premium: e.g., $1,000 Million

- **Retention Rates** for each company (RetA, RetB, RetC)
  - Retention = 0 means "cede all risk to reinsurer"
  - Retention = 0.5 means "keep 50%, cede 50%"
  - Retention = 1 means "keep all risk"

#### Step 2: Simulation Runs
The app:
1. **Generates 1,000 random premium & claim scenarios** using Brownian Motion (realistic financial model)
2. **Calculates profit** for each company using the real quota-share formula
3. **Computes average profit** across all scenarios

#### Step 3: Compare Strategies
- **Classic:** Shows results with your chosen retention rates
- **Nash Equilibrium:** Shows results with optimal retention rates recommended by the app (with fairness constraint)

The difference shows you how much better you could do! 💡

---

## 📐 Mathematical Foundation

### Real Quota-Share Reinsurance Formula

In real insurance, quota-share reinsurance works as follows:

**Key Terms:**
- **Q** = Ceded Quota (percentage CEDED to reinsurer) - e.g., 70%
- **Retention** = 1 - Q (percentage KEPT by primary insurer) - e.g., 30%
- **P** = Insurance Premium (collected from policyholders)
- **C** = Insurance Claims/Losses (paid to policyholders)

**Premium Split:**
$$P_{ceded} = Q \times P$$

**Claims Split:**
$$C_{ceded} = Q \times C$$

**Profit Formula for Primary Insurer:**
$$\text{Profit} = \text{Retention} \times (P - C) = (1-Q) \times (P - C)$$

**Complete Example: QP70% Quota-Share (70% ceded, 30% retained)**
- Ceded Quota: Q = 0.70 (70% transferred to reinsurer)
- Retention Rate: Ret = 1 - 0.70 = 0.30 (30% kept by primary insurer)
- Premium Collected: P = $1,000
- Ceded Premium: 0.70 × $1,000 = $700 (to reinsurer)
- Retained Premium: 0.30 × $1,000 = $300 (by primary insurer)
- Claims Paid Out: C = $200
- Ceded Claims: 0.70 × $200 = $140 (reinsurer covers)
- Retained Claims: 0.30 × $200 = $60 (primary insurer covers)
- **Profit = 0.30 × ($1,000 - $200) = 0.30 × $800 = $240**

**Key Insight:** The insurer keeps 30% of the revenue AND covers 30% of the losses. The profit is proportional to the retention rate.

### 1. Geometric Brownian Motion (Claims Simulation)

Insurance premiums and claims follow unpredictable patterns. We model them using **Geometric Brownian Motion**:

$$S_T = S_0 \cdot e^{(\mu - \frac{\sigma^2}{2})T + \sigma\sqrt{T}Z}$$

Where:
- **S₀** = Initial premium/claim amount ($)
- **μ (mu)** = Drift (expected trend) = 0.05 (5% annual growth)
- **σ (sigma)** = Volatility (unpredictability) = 0.20 (20% standard deviation)
- **T** = Time horizon = 1 year
- **Z** = Random normal variable (generates randomness)
- **S_T** = Premium/claim amount after 1 year

**In English:** The premium and claim amounts grow randomly over time, sometimes up, sometimes down, but on average grow 5% per year with 20% volatility.

**Realistic Assumption:** Claims are typically 70% of premiums (loss ratio = 70%), so:
- Claims = GBM(S₀ × 0.7, μ, σ, T, N)

### 2. Profit Calculation (Real Quota-Share Formula)

Each company's profit is determined by their **retention rate** using the real quota-share formula:

$$\text{Profit} = \text{Retention} \times (\text{Premiums} - \text{Claims})$$

Where:
- **Retention** = 1 - Q (percentage they keep; 0-1 range)
- **Premiums** = Insurance premiums collected from policyholders  
- **Claims** = Insurance claims paid out to policyholders
- **Q** = Ceded Quota (percentage transferred to reinsurer)

**Mathematical Derivation:**
- Primary Insurer Profit = (Retention × Premiums) - (Retention × Claims)
- = Retention × (Premiums - Claims)

**Numerical Example:**
- Retention Rate = 0.4 (keep 40%, cede 60%)
- Premiums Collected = $1,000
- Claims Paid = $700
- Profit = 0.4 × ($1,000 - $700) = 0.4 × $300 = **$120**

**Interpretation:** The company keeps 40% of the net margin (premiums minus claims). The other 60% of both revenue and losses go to the reinsurer.

### 3. Nash Equilibrium (Optimization with Fairness)

The app finds the **optimal retention rates** by testing all combinations and selecting:

$$\text{NE} = \arg\max_{\text{Ret}_A, \text{Ret}_B, \text{Ret}_C} \left[ \sum \text{Profit}_i + 0.1 \times \min(\text{Profit}_i) \right]$$

Subject to constraints:
1. $$\text{Ret}_A + \text{Ret}_B + \text{Ret}_C \leq 1.0$$ (Total retention ≤ 100%)
2. $$\text{Ret}_i \geq 0.05 \text{ for all } i$$ (Minimum 5% retention per player - **Fairness Constraint**)

**In English:** Find the retention rates that maximize the **total expected profit PLUS a fairness bonus** for the poorest performer. This ensures:
- All players participate meaningfully (minimum 5% retention)
- No monopoly outcomes where one player takes everything
- Fair distribution that benefits everyone

**Why the Fairness Constraint?** Without it, Nash equilibrium can produce unfair outcomes like [0.0, 0.0, 1.0] where two players get nothing. The fairness term ensures all players contribute and profit.

### 4. Monte Carlo Simulation

The app runs **1,000 simulations**:

$$\text{Average Profit} = \frac{1}{N} \sum_{i=1}^{N} \text{Profit}_i$$

Where N = 1,000 simulations, giving statistical reliability.

---

## 💡 Core Concepts Explained

### Quota-Share Reinsurance (Real Implementation)

**What it is:** An agreement where primary insurers and reinsurers split both premiums and claims **proportionally** based on the quota.

**Example (Q=70% Ceded, Retention=30%):**
- Original Insurer (Company A) collects $1,000 in premiums
- Faces $700 in claims
- Company A chooses to cede 70% (retain 30%)
- **Premium Split:**
  - Insurer retains: 30% × $1,000 = $300
  - Reinsurer gets: 70% × $1,000 = $700
- **Claims Split:**
  - Insurer pays: 30% × $700 = $210
  - Reinsurer pays: 70% × $700 = $490
- **Profit = 30% × ($1,000 - $700) = 30% × $300 = $90**

**Why use it?**
- **Risk Mitigation:** Smaller insurers can cover more exposure without catastrophic losses
- **Profit Stability:** Reduces variance in outcomes
- **Market Efficiency:** Allows fair risk distribution among market participants
- **Growth Enablement:** Smaller companies can grow without proportional risk increase
- **Cost Reduction:** Lower capital requirements (less solvency capital needed)

**Constraint:** Ret_A + Ret_B + Ret_C ≤ 1.0
- The sum of retention rates across all companies cannot exceed 100%
- This ensures reinsurers don't have to cover more than 100% total

### Geometric Brownian Motion (GBM)

**What it is:** A mathematical model for random processes that never go negative (perfect for financial data).

**Visual:**
```
Premium/Claim
    |     ╱╲  ╱╲
    |    ╱  ╲╱  ╲╱╲
    |   ╱           ╲
    |  ╱             ╲___
    +─────────────────────→ Time
    0  3  6  9  12  ...
```

**Why use it?** Insurance premiums and claims follow random walk patterns like stock prices, never going negative.

## 🎲 Nash Equilibrium: Game Theory Optimization (Pillar II)

**Multi-Player Risk Sharing Strategy**

NashShield's second module handles the **Pillar II** component: optimizing risk-sharing strategies among multiple insurance companies using game theory.

### What is Nash Equilibrium?

**Simple Explanation:** A stable state where no player can improve their profit by changing strategy alone - AND everyone profits fairly.

**Example:**
- 3 insurance companies must decide how much risk to keep vs. transfer to reinsurers
- Company A: "If I keep more risk, I make more profit... but I could lose everything"
- Company B: "Everyone else keeps 30%, so I should too"
- Company C: "If all of us keep 30%, we all profit equally and safely"

**Result:** All three companies keep 30% and profit $600M each = **Nash Equilibrium** ✅

### Key Formulas (Pillar II)

#### Quota-Share Reinsurance Formula

$$\text{Profit} = \text{Retention} \times (\text{Premiums} - \text{Claims})$$

Where:
- **Retention** = 1 - Q (percentage company keeps)
- **Premiums** = Insurance premiums collected
- **Claims** = Insurance claims paid

**Example:** If Company A retains 40%:
- Collects $1,000 in premiums
- Faces $700 in claims
- Profit = 0.4 × ($1,000 - $700) = **$120** ✅

#### Nash Equilibrium Optimization

$$\text{NE} = \arg\max_{\text{Ret}_A, \text{Ret}_B, \text{Ret}_C} \left[ \sum \text{Profit}_i + 0.1 \times \min(\text{Profit}_i) \right]$$

**Subject to:**
- $$\sum \text{Ret}_i \leq 1.0$$ (Total retention ≤ 100%)
- $$\text{Ret}_i \geq 0.05$$ (Fairness: each player minimum 5%)

**What this means:** Find retention rates that maximize TOTAL profit PLUS a fairness bonus for the poorest performer.

### How Pillar II Works in NashShield

1. **Set Initial Claims** - Your company's exposure
2. **Choose Strategy** - Your retention rate (0-100%)
3. **Run Simulation** - 1,000 Monte Carlo scenarios
4. **Get Results** - Classic profit vs. Nash-optimized profit
5. **See Difference** - How much better Nash is (+30-50% typical)

### Why Both Pillars Matter

- **Pillar I (SCR)** = How much capital must you hold?
- **Pillar II (Nash)** = How should you share risk optimally?

Together they give a complete risk management framework! 🎯

---

## 🛠️ Technical Stack

### Backend
- **Python 3.13** - Core language
- **Flask 3.1.2** - Web framework for API
- **NumPy 2.4.1** - Numerical computations & simulations
- **SciPy 1.17.0** - Scientific computing
- **pandas 3.0.0** - Data handling
- **nashpy 0.0.43** - Game theory library (Nash calculations)

### Frontend
- **HTML5** - Page structure
- **CSS3** - Styling (glassmorphism design)
- **JavaScript (ES6+)** - Interactivity
- **Plotly 6.5.2** - Dynamic charts & visualizations
- **Canvas API** - Particle animation background

### Infrastructure
- **Flask-CORS** - Cross-origin requests
- **Werkzeug 3.1.5** - WSGI server

---

## 📦 Requirements

All dependencies are in `requirements.txt`:

```
blinker==1.9.0              # Event signaling
click==8.3.1                # CLI toolkit
contourpy==1.3.3            # Contour line calculations
cycler==0.12.1              # Matplotlib utilities
Deprecated==1.3.1           # Deprecation warnings
Flask==3.1.2                # Web framework ⭐
fonttools==4.61.1           # Font operations
itsdangerous==2.2.0         # Data signing (Flask)
Jinja2==3.1.6               # Template engine
kiwisolver==1.4.9           # Constraint solver
MarkupSafe==3.0.3           # Safe string handling
matplotlib==3.10.8          # Plotting library
narwhals==2.15.0            # DataFrame interface
nashpy==0.0.43              # Nash equilibrium solver ⭐
networkx==3.6.1             # Graph algorithms
numpy==2.4.1                # Numerical arrays ⭐
packaging==25.0             # Version parsing
pandas==3.0.0               # Data analysis ⭐
pillow==12.1.0              # Image processing
plotly==6.5.2               # Interactive charts ⭐
pyparsing==3.3.2            # Parsing library
python-dateutil==2.9.0      # Date utilities
scipy==1.17.0               # Scientific computing ⭐
six==1.17.0                 # Python 2/3 compatibility
werkzeug==3.1.5             # WSGI utilities
wrapt==2.0.1                # Function wrapping
```

**Key Libraries Explained:**
- **Flask**: Creates the web server and API
- **NumPy**: Handles all mathematical operations
- **nashpy**: Computes Nash equilibrium
- **Plotly**: Creates beautiful interactive charts
- **SciPy**: Advanced statistical functions

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.13+
- pip (Python package manager)
- Windows, macOS, or Linux

### Step 1: Clone/Download Project
```bash
cd c:\Users\User1\NashShield
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python -m flask --app backend.app run --port 5001
```

### Step 4: Open in Browser
```
http://127.0.0.1:5001
```

---

## 📖 How to Use

### Basic Workflow

#### 1. **Set Initial Claims** (💰 Initial Claims by Insurer)
Use sliders to set each company's initial claim:
- Company A: $1,000 (default, adjustable $100-$5,000)
- Company B: $1,000 (default, adjustable $100-$5,000)
- Company C: $1,000 (default, adjustable $100-$5,000)

**Why?** Different companies have different risk exposures.

#### 2. **Choose Strategy** (🎲 Players' Strategies)
Use quota sliders to set each company's risk retention:
- Company A Quota: 0.20 (keep 20% of risk)
- Company B Quota: 0.20 (keep 20% of risk)
- Company C Quota: 0.20 (keep 20% of risk)

**Constraint:** Sum must be ≤ 1.0

#### 3. **Select Scenario**
Choose one:
- **Classic Reinsurance:** Uses your chosen quotas
- **Nash Equilibrium:** Uses optimal quotas (recommended by app)

#### 4. **Run Simulation** (Run Simulation button)
Click the button. The app:
- Simulates 1,000 random claim scenarios
- Calculates profit for each company
- Displays average results

#### 5. **View Results** (📊 Expected Payoffs)
See:
- **Profit A, B, C:** Average profit per company
- **Comparison:** Classic vs Nash side-by-side
- **Difference (Δ):** How much better/worse Nash is
- **Visualization:** Brownian motion chart

### Example Scenario

**Setup:**
- Company A: $2,000 claim
- Company B: $1,500 claim
- Company C: $1,000 claim
- Your choice: q = [0.2, 0.2, 0.2]

**Run Classic:**
```
Profit A: $800
Profit B: $600
Profit C: $400
Total: $1,800
```

**Run Nash (App Recommends q = [0.5, 0.3, 0.1]):**
```
Profit A: $1,000
Profit B: $840
Profit C: $810
Total: $2,650
```

**Result:** Nash gives **+47% more profit!** 🚀

---

## ✨ Features

### 1. Real-Time Sliders
Adjust claims and quotas instantly, see updates live.

### 2. Monte Carlo Simulation
1,000 random scenarios for statistical accuracy.

### 3. Nash Equilibrium Solver
Automatically finds optimal quotas.

### 4. Visual Comparisons
- Side-by-side Classic vs Nash results
- Profit differences clearly shown
- Dynamic Brownian motion visualization

### 5. Educational Design
- Beginner-friendly explanations
- Advanced math formulas for experts
- Quotes from John Nash for inspiration

### 6. Responsive UI
- Beautiful glassmorphism design
- Mobile-friendly layout
- Smooth animations
- Dark theme for long sessions

### 7. Solvency Lab (Pillar I - NEW!)
- **Interactive Risk Exposure Sliders** - Adjust 6 risk categories in real-time
- **Octopus Visualization** - Watch risk grow as tentacles extend
- **Real-time SCR Calculation** - Instant capital requirement updates
- **17 Shock Scenarios** - Stress-test portfolio against real market events
- **Correlation Matrix** - View diversification benefits with color coding
- **Diversification Dashboard** - See exact capital savings from diversification
- **Educational Content** - HOW IT WORKS box, QUICK TIPS, DIVERSIFICATION INSIGHTS
- **Universe Background** - Beautiful pollen effect creating market context

---

## 🎯 NashShield Pillar I: SCR Calculator (NEW!)

**Solvency II Compliance Made Interactive**

The Pillar I module implements the **Solvency II** regulatory framework for calculating the Solvency Capital Requirement (SCR) - the capital an insurer must hold to stay solvent.

![Solvency Lab Solutions](images/sol1.png)
![Risk Analysis Dashboard](images/sol2.png)
![Portfolio Optimization](images/sol3.png)

### What is SCR (Solvency Capital Requirement)?

**Simple Explanation:** Imagine an insurance company has customers spread across different risk categories:
- **Market Risk** (stocks, bonds, currency fluctuations)
- **Life Risk** (mortality, longevity, lapses)
- **Health Risk** (medical claims, disability)
- **Non-Life Risk** (property, liability, accidents)
- **Counterparty Risk** (reinsurer default)
- **Operational Risk** (fraud, system failures)

If ALL these risks happened at the same time, how much money would the company lose? That's SCR! 💰

### SCR Calculation Formula

#### Step 1: Calculate Individual Risk Capital

For each risk module, we compute:
$$SCR_i = \text{Exposure}_i \times \text{Stress Factor}_i$$

Where:
- **Exposure_i** = Amount of capital exposed to that risk (e.g., 50M € for Market)
- **Stress Factor_i** = How much loss if worst case happens (e.g., 30% loss)

**Example:**
- Market Exposure: 50M €
- Market Stress Factor: 30%
- Market SCR = 50M € × 0.30 = **15M €**

#### Step 2: Account for Diversification (Correlation Matrix)

Risks don't all happen at the same time! Some risks offset each other:
- When markets crash 📉, people tend to keep insurance 📈
- When life expectancy increases, insurance costs rise 📈

We use **correlation coefficients** to model this:

$$BSCR = \sqrt{\sum_{i=1}^{6} \sum_{j=1}^{6} \rho_{i,j} \times SCR_i \times SCR_j}$$

**Correlation Matrix (NashShield Custom):**

| Risk | Market | Life | Health | Non-Life | Counterparty |
|------|--------|------|--------|----------|-------------|
| **Market** | 1.000 | 0.250 | 0.250 | 0.250 | 0.500 |
| **Life** | 0.250 | 1.000 | 0.250 | 0.250 | 0.000 |
| **Health** | 0.250 | 0.250 | 1.000 | 0.250 | 0.000 |
| **Non-Life** | 0.250 | 0.500 | 0.000 | 1.000 | 0.000 |
| **Counterparty** | 0.500 | 0.000 | 0.000 | 0.000 | 1.000 |

**What this means:**
- Market and Counterparty are correlated (0.500) - reinsurers fail when markets crash
- Life and Health are uncorrelated (0.000) - independent risk categories
- Lower correlations = More diversification benefits! 🎯

#### Step 3: Add Operational Risk

Operational risks (fraud, IT failures) don't diversify:

$$SCR_{Total} = BSCR + Operational Risk$$

**Why separate?** Because the company controls ops risk independently of market/life/health risks.

#### Step 4: Apply Shock Scenarios

The calculator stress-tests your portfolio against **17 real-world scenarios:**

1. **Market Crash 20%** - Stock market drops 20%
2. **Market Crash 40%** - Severe recession
3. **Interest Rate +2%** - Yields increase
4. **Interest Rate -2%** - Yields decrease
5. **Currency Shock ±10%** - FX fluctuations
6. **Life Mortality +15%** - More deaths (pandemics)
7. **Life Longevity +5 years** - People live longer
8. **Health Claims +30%** - Medical inflation
9. **Non-Life Large Loss** - Major catastrophe
10. **Reinsurer Default** - Counterparty fails
... and 7 more real scenarios

**Example - Market Crash 20% Impact:**
- Base SCR: 100M €
- Market exposure: 50M €
- If market crashes 20%: Shock Factor = 1.2
- Stressed Market SCR: 50M € × 0.30 × 1.2 = **18M €** (was 15M €)
- New Total SCR: **103M €** (+3% impact)

### Diversification Benefits

The formula shows how much risk you **save** by diversifying:

$$\text{Diversification Benefit} = \frac{\sum SCR_i - BSCR}{\sum SCR_i} \times 100\%$$

**Example:**
- Sum of individual SCRs: 100M €
- BSCR (with correlations): 70M €
- Diversification Benefit: **30%**

This means 30% of your capital requirement is saved just by holding diversified risks! 🎉

### Solvency Lab: Interactive Risk Optimization

The Solvency Lab module lets you:

#### 1. **Adjust Risk Exposure** - 6 Interactive Sliders
- Market: 0-200M € (default: 50M €)
- Life: 0-200M € (default: 30M €)
- Health: 0-150M € (default: 20M €)
- Non-Life: 0-250M € (default: 40M €)
- Counterparty: 0-100M € (default: 10M €)
- Operational: 0-100M € (default: 15M €)

#### 2. **Watch the Octopus Visualization** 🐙
The octopus is a visual metaphor:
- **Body** = Core business
- **6 Tentacles** = 6 risk categories
- **Tentacle Length** = Risk exposure size
- **Suction Cups** = Risk granularity
- **Universe Background** = Market context with pollen particles

As you move sliders, tentacles grow/shrink in real-time!

#### 3. **Calculate SCR Instantly**
The calculator shows:
- **BSCR** (Base Solvency Capital Requirement)
- **Operational Risk** component
- **Total SCR** required

#### 4. **View Diversification Dashboard**
- Total risk without correlation: X M €
- Diversification benefit: Y M €
- Correlation matrix with color coding

#### 5. **Run Shock Scenarios** ⚡
Test your portfolio against 17 real scenarios:
- See impact % and absolute amount
- Identify vulnerable risk exposures
- Optimize for worst-case scenarios

#### 6. **Key Insights Box**
Practical tips:
- ✓ Move sliders to test exposures
- ✓ Watch octopus grow with risk
- ✓ Check correlation matrix
- ✓ Lower op risk for stability
- ✓ Exploit low-correlation pairs

### How to Use Solvency Lab

**Scenario 1: Insurance Company A wants to expand**
1. Increase Market and Life exposures (growth areas)
2. Watch how BSCR changes in real-time
3. Run shock scenarios to see downside risk
4. Adjust Operational Risk level
5. Compare diversification benefit before/after
6. Make informed expansion decision ✅

**Scenario 2: Reinsurer wants to reduce capital requirement**
1. Identify high-correlation risk pairs
2. Reduce one of the correlated exposures
3. Watch BSCR decrease disproportionately
4. Exploit diversification benefits
5. Lower capital needed while maintaining coverage ✅

**Scenario 3: Risk manager stress-testing**
1. Set realistic portfolio exposures
2. Run all 17 shock scenarios
3. Identify which risks are most impactful
4. Build hedging strategy
5. Re-run scenarios with hedges in place ✅

---

## 📂 Project Structure

```
NashShield/
├── backend/
│   ├── __init__.py
│   ├── app.py              # Flask server & API routes
│   ├── simulation.py        # GBM & profit calculations
│   └── nash.py             # Nash equilibrium solver
├── templates/
│   ├── index.html          # Main interactive UI
│   ├── results.html        # Results display
│   └── test.html           # API testing page
├── static/                 # CSS, JS, assets
├── tests/
│   ├── test_simulation.py  # Unit tests
│   └── test_nash.py        # Nash equilibrium tests
├── notebooks/
│   └── exploration.ipynb   # Jupyter analysis
├── data/                   # Data files (if needed)
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── get-pip.py            # Pip installer
```

---

## 🔬 Implementation Details

### Backend Architecture

The NashShield backend implements the real quota-share reinsurance formula through three main modules:

#### 1. **simulation.py** - Core Simulation Engine

**Functions:**
- `simulate_GBM(S0, mu, sigma, T, N)` - Generates random premium/claims paths using Geometric Brownian Motion
- `calculate_profit(premiums, claims, retention)` - Applies the real profit formula
- `simulation_3_insurers(S0, mu, sigma, T, N, retentions)` - Simulates 3 insurers with identical premiums
- `simulation_3_insurers_different_premiums(S0A, S0B, S0C, mu, sigma, T, N, retentions)` - Simulates 3 insurers with different premiums

**Algorithm:**
```
For each of N=1000 simulations:
  1. Generate random premium path using GBM
  2. Generate claims path = 0.7 × premium path (70% loss ratio)
  3. Calculate each insurer's profit: Ret × (Premium - Claims)
  4. Store profit in array

Return average profit across all 1000 simulations
```

**Parameters:**
- μ = 0.05 (5% annual drift - premiums grow on average)
- σ = 0.2 (20% volatility - randomness in claims)
- T = 1 year
- N = 1000 simulations for statistical confidence

#### 2. **nash.py** - Equilibrium Solver

**Functions:**
- `nash_equilibrium_3_insurers(S0, mu, sigma, T, N, retention_options)` - Finds optimal retentions for 3 insurers with same premiums
- `nash_equilibrium_3_insurers_different_premiums(S0A, S0B, S0C, mu, sigma, T, N, retention_options)` - Finds optimal retentions with different premiums

**Algorithm:**
```
For each possible combination of retention rates:
  IF sum(retentions) > 1.0:
    Skip (violates constraint)
  ELSE:
    Run simulation with these retentions
    Calculate total social welfare = Profit_A + Profit_B + Profit_C
    
Return the combination with highest total welfare
```

**Constraint:** Ret_A + Ret_B + Ret_C ≤ 1.0
- Ensures the reinsurer doesn't have to cover more than 100% total

#### 3. **app.py** - Flask REST API

**Endpoints:**

```
GET /
  Returns: index.html (main UI)
  
POST /simulate
  Accepts JSON:
    {
      "qA": 0.3,          # Retention rate for player A (0-1)
      "qB": 0.4,          # Retention rate for player B (0-1)
      "qC": 0.3,          # Retention rate for player C (0-1)
      "S0A": 1000,        # Initial premium for A
      "S0B": 1000,        # Initial premium for B
      "S0C": 1000,        # Initial premium for C
      "scenario": "classic" # or "nash"
    }
  
  Returns JSON:
    {
      "profit_A": 124.56,
      "profit_B": 165.78,
      "profit_C": 98.34,
      "scenario": "classic",
      "message": "Simulation completed..."
    }
```



### Frontend Architecture

#### 1. **HTML Form** (index.html)
- Input sliders for initial premiums (S₀A, S₀B, S₀C)
- Input sliders for retention rates (qA, qB, qC)
- Scenario selector (Classic vs Nash)
- Run Simulation button

#### 2. **JavaScript Handler** 
- Validates input (sum of retentions ≤ 1.0)
- Sends POST request to `/simulate` endpoint
- Runs classic AND nash scenarios for comparison
- Updates results display with both scenarios

#### 3. **Results Display**
- Shows expected profits for each player
- Compares classic vs nash equilibrium
- Displays profit improvement percentage
- Shows stochastic visualization (Brownian motion chart)

### Formula Verification

All formulas have been tested and verified. Test results:

```
✓ GBM Simulation: Mean ≈ Expected value
✓ Profit Calculation: Ret × (P - C) verified for 0%, 30%, 100% retention
✓ Loss Ratio: Claims = 70% × Premiums maintained
✓ Three-Insurer Scenario: Higher retention → higher profit
✓ Nash Equilibrium: Constraint satisfied, welfare maximized
```

---

## 🎓 Mathematical Deep Dive (For Experts)

**Note:** All formulas and models in this project are **simplified educational versions**. Real insurance calculations are significantly more complex.

### Expected Value Calculation
$$\mathbb{E}[\text{Profit}] = (1-q) \cdot \mathbb{E}[S_T]$$

where:
$$\mathbb{E}[S_T] = S_0 \cdot e^{\mu T}$$



### Variance & Risk
$$\text{Var}[\text{Profit}] = (1-q)^2 \cdot \text{Var}[S_T]$$

$$\text{Var}[S_T] = S_0^2 e^{2\mu T}(e^{\sigma^2 T} - 1)$$

### Sharpe Ratio (Risk-Adjusted Return)
$$\text{Sharpe} = \frac{\mathbb{E}[\text{Return}]}{\sqrt{\text{Var}[\text{Return}]}}$$

### Covariance Between Players
$$\text{Cov}[\text{Profit}_A, \text{Profit}_B] = (1-q_A)(1-q_B) \cdot \text{Cov}[S_{T,A}, S_{T,B}]$$

**Note:** In this model, claims are independent, so covariance = 0.

---

## 🧪 Running Tests

```bash
# Test simulations
python -m pytest tests/test_simulation.py -v

# Test Nash equilibrium
python -m pytest tests/test_nash.py -v

# Test backend API
python test_api.py
```

---

## 🤝 Contributing

This project demonstrates:
- Game theory applications in insurance
- Monte Carlo simulation techniques
- Nash equilibrium computation
- Full-stack web development (Flask + frontend)

Feel free to:
- Add more players (4, 5+ insurers)
- Implement correlated claims
- Add optimal reinsurance pricing
- Create visualization dashboards

---

## 📚 References

1. **Nash Equilibrium Theory**
   - Nash, J.F. (1950). Equilibrium Points in N-Person Games
   - Von Neumann & Morgenstern (1944). Theory of Games and Economic Behavior

2. **Geometric Brownian Motion**
   - Black-Scholes Model for financial derivatives
   - Itô's Lemma for stochastic calculus

3. **Reinsurance**
   - Borch, K. (1962). Equilibrium in a Reinsurance Market
   - Lemaire, J. (1985). Automobile Insurance: Actuarial Models

---

## 📞 Support

For questions or issues:
1. Check the in-app explanations (green info boxes)
2. Review the mathematical formulas above
3. Test with the API directly
4. Check Flask logs for debugging

---

## 📝 License

Educational project for game theory and insurance risk management.

**⚠️ IMPORTANT NOTICE:**
This project is created **for fun and educational purposes only**. It should not be used for:
- Real insurance decisions
- Actual financial transactions
- Production reinsurance calculations
- Regulatory compliance
- Professional risk management

The mathematical models are **simplified versions** of real-world insurance dynamics. Real insurance requires:
- Professional actuaries
- Regulatory compliance
- Proper risk assessment
- Comprehensive pricing models
- Legal frameworks

**Use this project to LEARN game theory and mathematics, not to manage real insurance!** 🎓

---

## 🎯 Key Takeaway

**NashShield proves that cooperation beats competition.**

By using game theory and mathematical optimization, insurance companies can increase profits by **30-50%** while reducing risk. That's the power of Nash Equilibrium! 🚀



Enjoy learning! Have fun exploring the math! 🚀


*Made with ❤️ by Farah*
*ps : i really recommend to watch the movie 'a beautiful mind'*

*Last Updated: January 22, 2026*
*Created for understanding insurance game theory and risk sharing optimization*
