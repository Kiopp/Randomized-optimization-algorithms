import itertools
import time
from solver import solve_aco
def tune_aco_parameters(problem, param_grid, num_runs=3):
    """
    Performs a grid search to find the best ACO hyperparameters.
    Runs each combination multiple times to account for ACO's randomness.
    """
    # Extract parameter names and their list of values to test
    keys = list(param_grid.keys())
    values = list(param_grid.values())
    
    # Generate all possible combinations of the parameters
    combinations = list(itertools.product(*values))
    
    best_overall_cost = float('inf')
    best_params = None
    results_log = []
    
    print("-" * 50)
    print(f"Starting Grid Search: {len(combinations)} combinations to test.")
    print(f"Averaging over {num_runs} runs per combination.")
    print("-" * 50)
    
    for idx, combo in enumerate(combinations):
        current_params = dict(zip(keys, combo))
        print(f"[{idx + 1}/{len(combinations)}] Testing: {current_params}")
        
        total_cost_for_combo = 0.0
        start_time = time.time()
        
        for run in range(num_runs):
            # We use **current_params to unpack the dictionary directly into the function arguments
            _, cost, _ = solve_aco(problem, **current_params)
            total_cost_for_combo += cost
            
        elapsed_time = time.time() - start_time
        avg_cost = total_cost_for_combo / num_runs
        
        results_log.append({
            'params': current_params,
            'avg_cost': avg_cost,
            'time_taken': elapsed_time
        })
        
        print(f"  -> Avg Cost: {avg_cost:.2f} | Time: {elapsed_time:.2f}s")
        
        if avg_cost < best_overall_cost:
            best_overall_cost = avg_cost
            best_params = current_params
            print(f"  *** New Best Parameters Found! ***")
            
    print("-" * 50)
    print("TUNING COMPLETE")
    print(f"Best Parameters: {best_params}")
    print(f"Best Average Cost: {best_overall_cost:.2f}")
    print("-" * 50)
    
    return best_params, best_overall_cost, results_log