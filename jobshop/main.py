import parse
import trejectory
import population
import statistics

def main():
    print("Simmulated annealing:")
    test_trejectory(10, 'ft06', 55)
    test_trejectory(10, 'la03', 597)
    test_trejectory(10, 'swv10', 1767)
    
    print("(μ+λ) Evolution strategy:")
    test_population(10, 'ft06', 55)
    test_population(10, 'la03', 597)
    test_population(5, 'swv10', 1767) # Fewer runs because it is super slow

def test_trejectory(n_tests, instance_key='abz5', known_best=0):
    # Initialize parameters
    makespans = []
    ins = parse.parse_jsp_instances("jobshop.txt")
    prev_best = 9999999999
    prev_best_sol = []

    # Run algorithm n_tests times keeping track of the best solution and makespans
    for i in range(n_tests):
        best_solution, best_makespan, _ = trejectory.simulated_annealing(ins[instance_key], quiet=True)
        if best_makespan < prev_best:
            prev_best = best_makespan
            prev_best_sol = best_solution
        makespans.append(best_makespan)

    # Calculate interesting statistics
    avg = statistics.mean(makespans)
    avg_diff = 100 * (1 - (known_best / avg))

    # Print results
    print(f'Testing {instance_key} using simulated annealing')
    print(f'Average makespan over {n_tests} runs: {avg} (known_best={known_best})')
    print(f'Average diff from known best: {avg_diff:.2f}%')
    print(f'Best makespan from all runs: {prev_best}')
    print(f'Best solution: {prev_best_sol}\n')

def test_population(n_tests, instance_key='abz5', known_best=0):
    # Initialize parameters
    makespans = []
    ins = parse.parse_jsp_instances("jobshop.txt")
    prev_best = 9999999999
    prev_best_sol = []

    # Run algorithm n_tests times keeping track of the best solution and makespans
    for i in range(n_tests):
        best_solution, best_makespan, _ = population.solve_mu_plus_lambda(ins[instance_key])
        if best_makespan < prev_best:
            prev_best = best_makespan
            prev_best_sol = best_solution
        makespans.append(best_makespan)

    # Calculate interesting statistics
    avg = statistics.mean(makespans)
    avg_diff = 100 * (1 - (known_best / avg))
    
    # Print results
    print(f'Testing {instance_key} using (μ+λ) evolution strategy')
    print(f'Average makespan over {n_tests} runs: {avg} (known_best={known_best})')
    print(f'Average diff from known best: {avg_diff:.2f}%')
    print(f'Best makespan from all runs: {prev_best}')
    print(f'Best solution: {prev_best_sol}\n')

main()