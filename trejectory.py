import random
import math
import copy
import parse
import helper

def simulated_annealing(instance, t_start=1000, t_stop=0.01, cooling_rate=0.9999, max_iterations=200000, quiet=False):
    # Initial solution
    history = []
    current_solution = helper.random_solution(instance)
    current_makespan = helper.makespan(instance, current_solution)
    best_solution = current_solution[:]
    best_makespan = current_makespan

    history.append(best_makespan) # Saves history for plots

    t = t_start
    current_iteration = 0

    for i in range(max_iterations):
        # Generate candidate by swapping two random elements of the current solution
        new_solution = helper.swap(current_solution)
        new_makespan = helper.makespan(instance, new_solution)

        # Find the difference between the new and the old makespan
        diff = new_makespan - current_makespan

        # Check if solution should be accepted;
        # 1. If the diff is less than 0 (negative), it is a better solution
        # 2. Sometimes accept a worse solution depending on the tempearture
        if diff < 0 or random.random() < math.exp(-diff / t):
            # Update current solution
            current_solution = new_solution
            current_makespan = new_makespan

            # Update best solution
            if current_makespan < best_makespan:
                best_solution = current_solution[:]
                best_makespan = current_makespan
                history.append(best_makespan) # Saves history for plots

        t *= cooling_rate # Cool down the temperature by the cooling rate factor.

        # Check stop conditions;
        # 1. Check if max iterations are reached
        if i == max_iterations - 1 and not quiet:
            print(f'Ran out of iterations!(temp: {t})')

        # 2. Check if temperature is too low
        if t < t_stop:
            if not quiet: 
                print(f'Temperature too low! (iteration: {i})')
            break
    return best_solution, best_makespan, history