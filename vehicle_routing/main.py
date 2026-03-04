from process import *
from solver import solve_aco, solve_grasp
from plotting import *
from tuning import *

def main():
    #cvrp()
    #vrptw()
    run_tuning()

def cvrp():
    with open('cvrp.txt', 'r') as file:
        cvrp_text = file.read()
    problem = parse_cvrp(cvrp_text)

    aco_routes, aco_cost, history = solve_aco(problem)

    grasp_routes, grasp_cost = solve_grasp(problem)

    print_comparative_summary("CVRP", grasp_routes, grasp_cost, aco_routes, aco_cost)

    plot_routes(problem, grasp_routes, f"CVRP GRASP Solution (cost: {grasp_cost:.2f})")
    plot_routes(problem, aco_routes, f"CVRP ACO Solution (cost: {aco_cost:.2f})")

    plot_convergence(history, grasp_cost)

def vrptw():
    with open('vrptw.txt', 'r') as file:
        vrptw_text = file.read()
    problem = parse_vrptw(vrptw_text)

    aco_routes, aco_cost, history = solve_aco(problem)

    grasp_routes, grasp_cost = solve_grasp(problem)

    print_comparative_summary("VRPTW", grasp_routes, grasp_cost, aco_routes, aco_cost)

    plot_routes(problem, grasp_routes, f"VRPTW GRASP Solution (cost: {grasp_cost:.2f})")
    plot_routes(problem, aco_routes, f"VRPTW ACO Solution (cost: {aco_cost:.2f})")

    plot_convergence(history, grasp_cost)

def run_tuning():
    param_grid = {
        'num_ants': [10, 20],               # Number of ants per iteration
        'num_iterations': [20, 50],         # Keep low for tuning to save time
        'alpha': [1.0, 2.0],                # Pheromone importance
        'beta': [2.0, 5.0],                 # Heuristic importance
        'evaporation': [0.1, 0.5, 0.8],     # Pheromone decay rate
        'Q': [100, 1000]                    # Deposit multiplier
    }

    with open('vrptw.txt', 'r') as file:
        vrptw_text = file.read()
    vrptw_problem = parse_vrptw(vrptw_text)

    with open('cvrp.txt', 'r') as file:
        cvrp_text = file.read()
    cvrp_problem = parse_cvrp(cvrp_text)
    
    # Run the tuner
    print("---- CVRP ----")
    best_params, best_cost, log = tune_aco_parameters(cvrp_problem, param_grid, num_runs=3)

    print("---- VRPTW ----")
    best_params, best_cost, log = tune_aco_parameters(vrptw_problem, param_grid, num_runs=3)


main()