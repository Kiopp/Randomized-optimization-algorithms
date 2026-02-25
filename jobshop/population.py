import helper
import random

def solve_mu_plus_lambda(
    problem,
    mu=50,          # Size of the parent population
    lambda_=100,    # Number of offspring generated per generation
    generations=500,
    crossover_rate=0.85,
    mutation_rate=0.15,
    tournament_size=5,
    verbose=False,
    log_every=50,
):
    history = []
    rng = random.Random() 
    template = helper.chromosome_template(problem)

    required_counts = {}
    for g in template:
        required_counts[g] = required_counts.get(g, 0) + 1

    # Initialize parent population (size mu)
    population = [helper.random_chromosome(template, rng) for _ in range(mu)]
    fitness = [helper.makespan(problem, c) for c in population]

    # Track the absolute best
    best_idx = min(range(mu), key=lambda i: fitness[i])
    best = list(population[best_idx])
    best_cost = fitness[best_idx]
    history.append(best_cost) # Saves history for plots

    if verbose:
        print(f'Initial best makespan: {best_cost}', flush=True)

    for gen in range(1, generations + 1):
        offspring_population = []
        
        # Generate lambda offspring
        for _ in range(lambda_):
            # Select parents from the mu population
            p1 = helper.tournament_select(population, fitness, tournament_size, rng)
            p2 = helper.tournament_select(population, fitness, tournament_size, rng)

            # Crossover
            if rng.random() < crossover_rate:
                child = helper.multiset_order_crossover(p1, p2, required_counts, rng)
            else:
                child = list(p1)

            # Mutation
            helper.swap_mutation(child, mutation_rate, rng)
            offspring_population.append(child)
            
        # Evaluate the lambda offspring
        offspring_fitness = [helper.makespan(problem, c) for c in offspring_population]

        # Combine parents (mu) and offspring (lambda)
        combined_population = population + offspring_population
        combined_fitness = fitness + offspring_fitness

        # Truncation Selection: Sort the combined pool by fitness
        ranked_indices = sorted(range(mu + lambda_), key=lambda i: combined_fitness[i])

        # Keep the top mu individuals for the next generation
        population = [combined_population[i] for i in ranked_indices[:mu]]
        fitness = [combined_fitness[i] for i in ranked_indices[:mu]]

        # Update the best found solution
        # Since population is now sorted, index 0 is guaranteed to be the best of this generation
        if fitness[0] < best_cost: 
            best_cost = fitness[0]
            best = list(population[0])
            history.append(best_cost) # Saves history for plots

        if verbose and (gen % log_every == 0 or gen == generations):
            print(f'Generation {gen}/{generations}: best={best_cost}', flush=True)

    return best, best_cost, history