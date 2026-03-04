import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def plot_routes(problem, routes, title="VRP Solution"):
    """
    Plots the nodes and the vehicle routes on a 2D scatter plot.
    """
    plt.figure(figsize=(10, 8))
    
    # Plot all customer nodes
    cust_x = [node.x for node in problem.customers]
    cust_y = [node.y for node in problem.customers]
    plt.scatter(cust_x, cust_y, c='blue', marker='o', s=30, label='Customers', zorder=2)
    
    # Plot the depot
    plt.scatter(problem.depot.x, problem.depot.y, c='red', marker='s', s=100, label='Depot', zorder=3)
    
    # Draw the routes
    colors = cm.rainbow(np.linspace(0, 1, len(routes)))
    
    for route_idx, route in enumerate(routes):
        route_x = [problem.nodes[node_idx].x for node_idx in route]
        route_y = [problem.nodes[node_idx].y for node_idx in route]
        
        plt.plot(route_x, route_y, color=colors[route_idx], linewidth=1.5, 
                 alpha=0.7, label=f'Vehicle {route_idx + 1}', zorder=1)
        
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    
    # Place legend outside the plot if there are many vehicles
    if len(routes) <= 10:
        plt.legend()
    else:
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()



def plot_convergence(aco_cost_history, grasp_cost, title="ACO Convergence vs GRASP Baseline"):
    """
    Plots the cost improvement of ACO over iterations compared to the GRASP baseline.
    """
    plt.figure(figsize=(10, 6))
    
    iterations = range(1, len(aco_cost_history) + 1)
    
    # Plot ACO cost curve
    plt.plot(iterations, aco_cost_history, marker='o', markersize=4, 
             linestyle='-', color='purple', label='ACO Best Cost', linewidth=2)
    
    # Plot GRASP baseline as a horizontal line
    plt.axhline(y=grasp_cost, color='orange', linestyle='--', 
                label=f'GRASP Baseline ({grasp_cost:.2f})', linewidth=2)
    
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Iteration')
    plt.ylabel('Total Route Cost')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()



def print_comparative_summary(problem_name, grasp_routes, grasp_cost, aco_routes, aco_cost):
    print("-" * 50)
    print(f"RESULTS SUMMARY: {problem_name}")
    print("-" * 50)
    print(f"{'Metric':<20} | {'GRASP Baseline':<15} | {'ACO Solver':<15}")
    print("-" * 50)
    print(f"{'Total Cost':<20} | {grasp_cost:<15.2f} | {aco_cost:<15.2f}")
    print(f"{'Vehicles Used':<20} | {len(grasp_routes):<15} | {len(aco_routes):<15}")
    
    cost_diff = grasp_cost - aco_cost
    pct_improvement = (cost_diff / grasp_cost) * 100 if grasp_cost > 0 else 0
    
    print("-" * 50)
    if cost_diff > 0:
        print(f"ACO improved upon GRASP by {pct_improvement:.2f}% ({cost_diff:.2f} cost units).")
    else:
        print(f"GRASP outperformed or tied ACO by {-pct_improvement:.2f}%. (Try tuning ACO parameters!)")
    print("-" * 50)