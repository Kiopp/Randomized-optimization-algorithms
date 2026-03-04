from helper import *
import random

def solve_aco(problem, num_ants=30, num_iterations=200, alpha=1, beta=3, evaporation=0.9, Q=100):
    num_nodes = problem.num_nodes
    pheromones = [[1.0 for _ in range(num_nodes)] for _ in range(num_nodes)]
    
    best_routes = None
    best_cost = float('inf')

    history = []
    
    for iteration in range(num_iterations):
        all_ant_routes = []
        all_ant_costs = []
        
        for ant in range(num_ants):
            unvisited = set(range(1, num_nodes))
            routes = []
            
            while unvisited:
                current_route = [0]
                current_node = 0
                current_load = 0.0
                current_time = 0.0
                
                while True:
                    feasible_moves = []
                    for j in unvisited:
                        # Feasibility
                        feasible, new_load, new_time = is_feasible(
                            problem, current_node, j, current_load, current_time
                        )
                        if feasible:
                            feasible_moves.append((j, new_load, new_time))
                            
                    if not feasible_moves:
                        break # Must return to depot
                        
                    probabilities = []
                    total_prob = 0.0
                    for j, _, _ in feasible_moves:
                        tau = pheromones[current_node][j]
                        
                        # Heuristic (eta)
                        eta = calculate_heuristic(problem, current_node, j, current_time)
                        
                        prob = (tau ** alpha) * (eta ** beta)
                        probabilities.append(prob)
                        total_prob += prob
                        
                    # Roulette wheel selection
                    rand_val = random.uniform(0, total_prob)
                    cumulative = 0.0
                    chosen_idx = -1
                    for i, prob in enumerate(probabilities):
                        cumulative += prob
                        if cumulative >= rand_val:
                            chosen_idx = i
                            break
                            
                    next_node, current_load, current_time = feasible_moves[chosen_idx]
                    current_route.append(next_node)
                    unvisited.remove(next_node)
                    current_node = next_node
                    
                current_route.append(0)
                routes.append(current_route)
                
            # Evaluate total cost with penalties
            total_cost = evaluate_solution_cost(problem, routes)
            
            all_ant_routes.append(routes)
            all_ant_costs.append(total_cost)
            
            if total_cost < best_cost:
                best_cost = total_cost
                best_routes = routes
                
        # Pheromone Update (Evaporation & Deposit)
        for i in range(num_nodes):
            for j in range(num_nodes):
                pheromones[i][j] *= (1.0 - evaporation)
                
        for routes, cost in zip(all_ant_routes, all_ant_costs):
            # If the cost is heavily penalized, the deposit is tiny, effectively ignoring bad routes
            deposit = Q / cost 
            for route in routes:
                for i in range(len(route) - 1):
                    from_node = route[i]
                    to_node = route[i+1]
                    pheromones[from_node][to_node] += deposit
                    pheromones[to_node][from_node] += deposit

        history.append(best_cost)

    return best_routes, best_cost, history

def solve_grasp(problem, alpha=0.3):
    unvisited = set(range(1, problem.num_nodes))
    routes = []
    total_cost = 0.0
    
    while unvisited:
        current_route = [0] # Start at depot
        current_node = 0
        current_load = 0.0
        current_time = 0.0
        
        while True:
            candidates = []
            for j in unvisited:
                feasible, new_load, new_time = is_feasible(problem, current_node, j, current_load, current_time)
                if feasible:
                    cost = calculate_grasp_cost(problem, current_node, j, current_time)
                    candidates.append((cost, j, new_load, new_time))
            
            if not candidates:
                break # Route is done, must return to depot
            
            # Sort by greedy cost (distance)
            candidates.sort(key=lambda x: x[0])
            
            # Form Restricted Candidate List (RCL)
            min_cost = candidates[0][0]
            max_cost = candidates[-1][0]
            threshold = min_cost + alpha * (max_cost - min_cost)
            
            rcl = [c for c in candidates if c[0] <= threshold]
            
            # Pick randomly from RCL
            chosen = random.choice(rcl)
            _, next_node, current_load, current_time = chosen
            
            current_route.append(next_node)
            unvisited.remove(next_node)
            current_node = next_node
            
        current_route.append(0) # End at depot
        routes.append(current_route)
        
        # Calculate cost for this route
        for i in range(len(current_route) - 1):
            total_cost += problem.distance_matrix[current_route[i]][current_route[i+1]]
            
    return routes, total_cost