import random
import numpy as np
from typing import List
from itertools import combinations

class Individual:
    """Simple data structure to hold a chromosome and its evaluation metrics."""
    def __init__(self, facilities: List[int]):
        self.facilities = np.array(facilities)
        self.distance = float('inf')
        self.dispersion = 0.0
        self.violation = float('inf')
        self.rank = -1
        self.crowding_distance = 0.0

    def dominates(self, other) -> bool:
        # Less violation is always better
        if self.violation < other.violation:
            return True
        elif self.violation > other.violation:
            return False
        
        # Minimize distance, Maximize dispersion
        better_or_eq = (self.distance <= other.distance) and (self.dispersion >= other.dispersion)
        strictly_better = (self.distance < other.distance) or (self.dispersion > other.dispersion)
        
        return better_or_eq and strictly_better


def evaluate(ind: Individual, inst, dist_matrix: np.ndarray, customer_order: np.ndarray):
    facilities = ind.facilities
    dist = 0.0
    caps = np.full(inst.p, inst.capacity, dtype=float)
    
    # Calculate Distance objective and Violation constraint
    for c in customer_order:
        dists_to_open = dist_matrix[c, facilities]
        demand = inst.demand[c]
        
        valid_mask = caps >= demand
        if np.any(valid_mask):
            valid_indices = np.where(valid_mask)[0]
            best_idx = valid_indices[np.argmin(dists_to_open[valid_mask])]
            dist += dists_to_open[best_idx]
            caps[best_idx] -= demand
        else:
            best_idx = np.argmin(dists_to_open)
            dist += dists_to_open[best_idx]
            caps[best_idx] -= demand
            
    ind.distance = dist
    ind.violation = np.sum(np.maximum(0, -caps))
    
    # Calculate Dispersion objective
    if len(facilities) > 1:
        # Get distances between all unique pairs of chosen facilities
        pair_dists = [dist_matrix[f1, f2] for f1, f2 in combinations(facilities, 2)]
        ind.dispersion = min(pair_dists)
    else:
        ind.dispersion = 0.0


def initialize_population(pop_size: int, inst, dist_matrix: np.ndarray, customer_order: np.ndarray) -> List[Individual]:
    pop = []
    nodes = list(range(inst.n))
    for _ in range(pop_size):
        facs = random.sample(nodes, inst.p)
        ind = Individual(facs)
        evaluate(ind, inst, dist_matrix, customer_order)
        pop.append(ind)
    return pop

def initialize_unique_population(pop_size: int, inst, seen_solutions: set, dist_matrix: np.ndarray, customer_order: np.ndarray) -> List[Individual]:
    pop = []
    nodes = list(range(inst.n))
    while len(pop) < pop_size:
        facs = random.sample(nodes, inst.p)
        facs_key = tuple(sorted(facs))
        
        if facs_key not in seen_solutions:
            seen_solutions.add(facs_key)
            ind = Individual(facs)
            evaluate(ind, inst, dist_matrix, customer_order)
            pop.append(ind)
    return pop


def crossover(p1: Individual, p2: Individual, inst) -> Individual:
    union_facs = list(set(p1.facilities) | set(p2.facilities))
    if len(union_facs) < inst.p:
        remaining = list(set(range(inst.n)) - set(union_facs))
        union_facs += random.sample(remaining, inst.p - len(union_facs))
    
    child_facs = random.sample(union_facs, inst.p)
    return Individual(child_facs)


def mutate(ind: Individual, inst, mutation_rate: float):
    if random.random() < mutation_rate:
        facs = set(ind.facilities)
        remove_fac = random.choice(list(facs))
        facs.remove(remove_fac)
        candidates = list(set(range(inst.n)) - facs)
        facs.add(random.choice(candidates))
        ind.facilities = np.array(list(facs))


def fast_non_dominated_sort(pop: List[Individual]) -> List[List[Individual]]:
    fronts = [[]]
    for p in pop:
        p.domination_count = 0
        p.dominated_solutions = []
        for q in pop:
            if p.dominates(q):
                p.dominated_solutions.append(q)
            elif q.dominates(p):
                p.domination_count += 1
        if p.domination_count == 0:
            p.rank = 0
            fronts[0].append(p)
    
    i = 0
    while len(fronts[i]) > 0:
        next_front = []
        for p in fronts[i]:
            for q in p.dominated_solutions:
                q.domination_count -= 1
                if q.domination_count == 0:
                    q.rank = i + 1
                    next_front.append(q)
        i += 1
        fronts.append(next_front)
    return fronts[:-1]


def calculate_crowding_distance(front: List[Individual]):
    l = len(front)
    if l == 0: return
    for ind in front:
        ind.crowding_distance = 0.0
        
    for obj in ['distance', 'dispersion']: 
        front.sort(key=lambda x: getattr(x, obj))
        front[0].crowding_distance = float('inf')
        front[-1].crowding_distance = float('inf')
        
        obj_min = getattr(front[0], obj)
        obj_max = getattr(front[-1], obj)
        val_range = obj_max - obj_min
        if val_range == 0: continue
        
        for i in range(1, l - 1):
            front[i].crowding_distance += (getattr(front[i+1], obj) - getattr(front[i-1], obj)) / val_range


def tournament_selection(pop: List[Individual]) -> Individual:
    i, j = random.sample(pop, 2)
    if i.rank < j.rank:
        return i
    elif i.rank > j.rank:
        return j
    else:
        return i if i.crowding_distance > j.crowding_distance else j