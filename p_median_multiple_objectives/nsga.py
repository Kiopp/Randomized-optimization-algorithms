from helper import *

def solve_nsga2(inst, pop_size=100, generations=100, mutation_rate=0.1, verbose=True, unique=True) -> List[Individual]:
    # Precompute distance matrix and customer demands
    dist_matrix = np.linalg.norm(inst.xy[:, None, :] - inst.xy[None, :, :], axis=-1)
    customer_order = np.argsort(-inst.demand)

    # Track evaluated solutions using a sorted tuple as the hashable key
    seen_solutions = set()
    nodes = list(range(inst.n))
    
    # Initialize and sort first population
    if unique:
        pop = initialize_unique_population(pop_size, inst, seen_solutions, dist_matrix, customer_order)
    else:
        pop = initialize_population(pop_size, inst, dist_matrix, customer_order) # Does not guarantee unique population
    
    fast_non_dominated_sort(pop)
    
    # Evolution loop
    for gen in range(generations):
        offspring = []
        while len(offspring) < pop_size:
            p1 = tournament_selection(pop)
            p2 = tournament_selection(pop)

            child = crossover(p1, p2, inst)
            mutate(child, inst, mutation_rate)
            
            # Enforce uniqueness
            if unique:
                child_key = tuple(sorted(child.facilities))
                attempts = 0
                while child_key in seen_solutions and attempts < 10:
                    # Force a mutation to break out of duplicate state
                    mutate(child, inst, mutation_rate=1.0) 
                    child_key = tuple(sorted(child.facilities))
                    attempts += 1

                if child_key in seen_solutions:
                    # Inject a completely random unique alien if still stuck
                    while child_key in seen_solutions:
                        alien_facs = random.sample(nodes, inst.p)
                        child = Individual(alien_facs)
                        child_key = tuple(sorted(child.facilities))
                seen_solutions.add(child_key)

            evaluate(child, inst, dist_matrix, customer_order)
            offspring.append(child)
            
        combined = pop + offspring
        fronts = fast_non_dominated_sort(combined)
        
        new_pop = []
        for front in fronts:
            calculate_crowding_distance(front)
            if len(new_pop) + len(front) <= pop_size:
                new_pop.extend(front)
            else:
                front.sort(key=lambda x: x.crowding_distance, reverse=True)
                new_pop.extend(front[:pop_size - len(new_pop)])
                break
        pop = new_pop
        
        if verbose:
            feasible = [p for p in pop if p.violation == 0]
            best_dist = min([p.distance for p in feasible]) if feasible else "None"
            if gen % 10 == 0:
                print(f"Generation {gen} | Best Feasible Distance: {best_dist}")
            
    return pop