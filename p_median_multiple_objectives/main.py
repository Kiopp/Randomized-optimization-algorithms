import nsga
import parse

def main():
    instances = parse.load_instances("p_median_capacitated.txt")
    if instances:
        first_key = sorted(instances.keys())[0]
        inst = instances[first_key]

        print(f"\nNSGA-II on Instance {first_key} (n={inst.n}, p={inst.p})")
        for _ in range(1):

            final_population = nsga.solve_nsga2(inst, pop_size=50, generations=500, mutation_rate=0.2, verbose=True, unique=False)

            feasible_sols = [p for p in final_population if p.violation == 0]
            if feasible_sols:
                best_solution = min(feasible_sols, key=lambda x: x.distance)
                diff = 100 * (1-(inst.best_known / best_solution.distance))
                print(f"\nBest Feasible Distance Found: {best_solution.distance:.2f}")
                print(f"Best Feasible Dispersion Found: {best_solution.dispersion:.2f}")
                print(f"Target Best Known Distance: {inst.best_known} (Diff: {diff:.2f}%)")
            else:
                print("\nNo strictly feasible solution found.")

main()