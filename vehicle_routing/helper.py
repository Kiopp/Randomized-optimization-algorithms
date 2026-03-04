def calculate_heuristic(problem, current_node_idx, next_node_idx, current_time):
    """
    Calculates the heuristic desirability of moving to the next node.
    """
    dist = problem.distance_matrix[current_node_idx][next_node_idx]
    
    # Base case fallback to prevent division by zero
    if dist == 0:
        return 1.0 
    
    if problem.variant == 'vrptw':
        next_node = problem.nodes[next_node_idx]
        arrival_time = current_time + dist
        wait_time = max(0, next_node.tw_open - arrival_time)
        
        # In VRPTW, waiting is wasted time. We penalize distance and wait time.
        # 1e-6 to prevent division by zero
        return 1.0 / (dist + wait_time + 1e-6)
    elif problem.variant == 'cvrp':
        # Standard CVRP relies only on distance
        return 1.0 / dist

def evaluate_solution_cost(problem, routes, penalty_weight=10000.0):
    """
    Calculates the total cost of the routes and applies variant-specific penalties.
    """
    total_cost = 0.0
    
    # Calculate base distance cost
    for route in routes:
        for i in range(len(route) - 1):
            total_cost += problem.distance_matrix[route[i]][route[i+1]]
            
    # Apply VRPTW specific penalties
    if problem.variant == 'vrptw' and problem.num_vehicles is not None:
        if len(routes) > problem.num_vehicles:
            extra_vehicles = len(routes) - problem.num_vehicles
            # Heavy penalty to force ACO to find solutions within the vehicle limit
            total_cost += (extra_vehicles * penalty_weight)
            
    # If a future variant has unserved customer penalties, you would add them here.
            
    return total_cost

def is_feasible(problem, current_node_idx, next_node_idx, current_load, current_time):
    next_node = problem.nodes[next_node_idx]
    
    # Capacity Check
    if current_load + next_node.demand > problem.capacity:
        return False, 0, 0
    
    # Time Window Check for VRPTW
    travel_time = problem.distance_matrix[current_node_idx][next_node_idx]
    arrival_time = current_time + travel_time
    
    if problem.variant == 'vrptw':
        if arrival_time > next_node.tw_close:
            return False, 0, 0
        # Wait if arriving before time window opens
        wait_time = max(0, next_node.tw_open - arrival_time)
        new_time = arrival_time + wait_time + next_node.service_time
    elif problem.variant == 'cvrp':
        # In CVRP, time is total distance travelled
        new_time = arrival_time
        
    new_load = current_load + next_node.demand
    return True, new_load, new_time

def calculate_grasp_cost(problem, current_node_idx, next_node_idx, current_time):
    dist = problem.distance_matrix[current_node_idx][next_node_idx]
    
    if not problem.variant == 'vrptw':
        return dist # Standard CVRP just uses distance
        
    next_node = problem.nodes[next_node_idx]
    arrival_time = current_time + dist
    wait_time = max(0, next_node.tw_open - arrival_time)
    
    # Weight the cost: distance + waiting time + a penalty if the window closes soon
    urgency = next_node.tw_close - (arrival_time + wait_time)
    
    # You can tune these weights (alpha, beta, gamma) for better results
    return dist + wait_time + (1.0 / (urgency + 1.0))