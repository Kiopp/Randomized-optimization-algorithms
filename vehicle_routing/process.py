import math
import random
import copy

class Node:
    def __init__(self, id, x, y, demand=0, tw_open=0, tw_close=float('inf'), service_time=0):
        self.id = id
        self.x = x
        self.y = y
        self.demand = demand
        self.tw_open = tw_open
        self.tw_close = tw_close
        self.service_time = service_time

class ProblemInstance:
    def __init__(self, capacity, depot, customers, num_vehicles=None, variant='none'):
        self.capacity = capacity
        self.depot = depot
        self.customers = customers
        self.nodes = [depot] + customers
        self.num_vehicles = num_vehicles
        self.variant = variant
        self.num_nodes = len(self.nodes)
        self.distance_matrix = self._compute_distance_matrix()

    def _compute_distance_matrix(self):
        matrix = [[0.0 for _ in range(self.num_nodes)] for _ in range(self.num_nodes)]
        for i, n1 in enumerate(self.nodes):
            for j, n2 in enumerate(self.nodes):
                matrix[i][j] = math.hypot(n1.x - n2.x, n1.y - n2.y)
        return matrix

def parse_cvrp(text):
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    capacity = float(lines[0])
    depot_data = list(map(float, lines[1].split()))
    depot = Node(0, depot_data[0], depot_data[1])
    
    customers = []
    for i, line in enumerate(lines[2:], start=1):
        data = list(map(float, line.split()))
        customers.append(Node(i, data[0], data[1], demand=data[2]))
        
    return ProblemInstance(capacity, depot, customers, variant='cvrp')

def parse_vrptw(text):
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    header = list(map(float, lines[0].split()))
    num_vehicles, capacity = int(header[0]), header[1]
    
    depot_data = list(map(float, lines[1].split()))
    depot = Node(0, depot_data[0], depot_data[1])
    
    customers = []
    for i, line in enumerate(lines[2:], start=1):
        data = list(map(float, line.split()))
        customers.append(Node(i, data[0], data[1], demand=data[2], 
                              tw_open=data[3], tw_close=data[4], service_time=data[5]))
        
    return ProblemInstance(capacity, depot, customers, num_vehicles, variant='vrptw')