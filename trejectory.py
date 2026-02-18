import random
import math
import copy
import parse

def makespan(instance, solution):
    jobs = instance['jobs']
    machine_end_time = [0] * instance['n_machines'] # Time when each machine ends
    job_end_time = [0] * instance['n_jobs'] # Time when each job is free
    job_op = [0] * instance['n_jobs'] # Track operation step for each job

    for job_id in solution:
        next_op = job_op[job_id]

        machine_id, duration = jobs[job_id][next_op]

        start_time = max(machine_end_time[machine_id], job_end_time[job_id])
        end_time = start_time + duration

        machine_end_time[machine_id] = end_time
        job_end_time[job_id] = end_time
        job_op[job_id] += 1

    return max(machine_end_time)

def random_solution(instance):
    solution = []
    for i, job in enumerate(instance['jobs']):
        solution.extend([i] * len(job))

    random.shuffle(solution)
    return solution

def swap(solution):
    # Swap two random elements in the solution
    neighbor = solution[:]
    idx1, idx2 = random.sample(range(len(neighbor)), 2)
    neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
    return neighbor

def simulated_annealing(instance, t_start=100, t_stop=0.01, cooling_rate=0.99, max_iterations=1000, quiet=False):
    # Initial solution
    current_solution = random_solution(instance)
    current_makespan = makespan(instance, current_solution)
    best_solution = current_solution[:]
    best_makespan = current_makespan

    t = t_start
    current_iteration = 0

    for i in range(max_iterations):
        # Generate candidate
        new_solution = swap(current_solution)
        new_makespan = makespan(instance, new_solution)

        diff = new_makespan - current_makespan

        # Check if solution should be accepted
        if diff < 0 or random.random() < math.exp(-diff / t):
            # Update current solution
            current_solution = new_solution
            current_makespan = new_makespan

            # Update best solution
            if current_makespan < best_makespan:
                best_solution = current_solution[:]
                best_makespan = current_makespan

        t *= cooling_rate
        if i == max_iterations - 1 and not quiet:
            print(f'Ran out of iterations!(temp: {t})')
        if t < t_stop:
            if not quiet: 
                print(f'Temperature too low! (iteration: {i})')
            break
    return best_solution, best_makespan