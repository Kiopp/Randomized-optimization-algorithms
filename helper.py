import random

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

def chromosome_template(problem):
    template = []
    for job_id, ops in enumerate(problem['jobs']):
        template.extend([job_id] * len(ops))
    return template

def random_chromosome(template, rng):
    c = list(template)
    rng.shuffle(c)
    return c

def tournament_select(population, fitness, k, rng):
    best_idx = None
    for _ in range(k):
        idx = rng.randrange(len(population))
        if best_idx is None or fitness[idx] < fitness[best_idx]:
            best_idx = idx
    return list(population[best_idx])

def multiset_order_crossover(p1, p2, required_counts, rng):
    n = len(p1)
    a, b = sorted((rng.randrange(n), rng.randrange(n)))
    child = [-1] * n

    used = {k: 0 for k in required_counts}
    for i in range(a, b + 1):
        child[i] = p1[i]
        used[p1[i]] += 1

    fill_positions = [i for i, g in enumerate(child) if g == -1]
    fill_idx = 0
    for gene in p2:
        if used[gene] < required_counts[gene]:
            child[fill_positions[fill_idx]] = gene
            used[gene] += 1
            fill_idx += 1
            if fill_idx >= len(fill_positions):
                break

    if any(g == -1 for g in child):
        missing = []
        for gene, req in required_counts.items():
            diff = req - used[gene]
            if diff > 0:
                missing.extend([gene] * diff)
        rng.shuffle(missing)
        m = 0
        for i, g in enumerate(child):
            if g == -1:
                child[i] = missing[m]
                m += 1

    return child

def swap_mutation(chromosome, mutation_rate, rng):
    if rng.random() >= mutation_rate:
        return
    i = rng.randrange(len(chromosome))
    j = rng.randrange(len(chromosome))
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]