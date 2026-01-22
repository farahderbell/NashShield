import sys
sys.path.insert(0, 'c:\\Users\\User1\\NashShield')

try:
    from backend.simulation import simulation_3_assureurs
    print("✓ simulation_3_assureurs imported")
    
    from backend.nash import nash_equilibrium_3_assureurs
    print("✓ nash_equilibrium_3_assureurs imported")
    
    # Test a simple simulation  
    profit_A, profit_B, profit_C = simulation_3_assureurs(1000, 0.05, 0.2, 1, 100, [0.2, 0.2, 0.2])
    print(f"✓ Simulation works: {len(profit_A)} results")
    
    # Test Nash
    print("Testing Nash equilibrium...")
    quotas_options = [0.0, 0.1, 0.2, 0.3]
    best_quotas, profits = nash_equilibrium_3_assureurs(1000, 0.05, 0.2, 1, 100, quotas_options)
    print(f"✓ Nash works: {best_quotas}")
    
except Exception as e:
    import traceback
    print(f"✗ Error: {e}")
    traceback.print_exc()
