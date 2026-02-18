import parse
import trejectory
import statistics

def main():
    ins = parse.parse_jsp_instances("jobshop.txt")
    best_solution, best_makespan = trejectory.simulated_annealing(ins['la03'])
    print(best_solution)
    print(best_makespan)

def test(n_tests, instance_key='abz5', known_best=0):
    makespans = []
    ins = parse.parse_jsp_instances("jobshop.txt")
    
    for i in range(n_tests):
        _, best_makespan = trejectory.simulated_annealing(ins[instance_key])
        makespans.append(best_makespan)

    avg = statistics.mean(makespans)
    diff = avg - known_best
    print(f'Average makespan: {avg}')
    print(f'Diff from known best: {diff} (known_best={known_best})')

def test_all(n_tests):
    ins = parse.parse_jsp_instances("jobshop.txt")

    for key in ins:
        print(f'Test: {key}')
        makespans = []
        for i in range(n_tests):
            _, best_makespan = trejectory.simulated_annealing(ins[key], quiet=True)
            makespans.append(best_makespan)

        avg = statistics.mean(makespans)
        print(f'Average makespan: {avg}')

#test(20, 'la03', 597) # test la03 instance
#test_all(10)
main()