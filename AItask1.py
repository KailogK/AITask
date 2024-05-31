import random

# parameters
nodes = 13
colors = 4
population_size = 20
generations = 100
mutation_rate = 0.1
replacement_rate = 0.3

# colors - 0: Blue, 1: Red, 2: Green, 3: Yellow
colors = [0, 1, 2, 3]

# dictionary for adjacent nodes
adjacency_list = {
    1: [2, 3, 12],
    2: [1, 3, 4, 11, 12],
    3: [1, 2, 4, 5, 6, 7],
    4: [2, 3, 7, 9],
    5: [3, 6],
    6: [3, 5, 7],
    7: [3, 4, 6, 8, 9],
    8: [7, 9, 10],
    9: [4, 7, 8, 10, 11],
    10: [8, 9, 11, 13],
    11: [2, 9, 10, 12, 13],
    12: [1, 2, 11, 13],
    13: [10, 11, 12]
}

# generate initial population
def generate_population(size, nodes, colors):
    return [[random.choice(colors) for _ in range(nodes)] for _ in range(size)]

# fitness function
def fitness(chromosome):
    conflicts = 0
    for node, neighbors in adjacency_list.items():
        for neighbor in neighbors:
            if chromosome[node-1] == chromosome[neighbor-1]:
                conflicts += 1
    return conflicts

# roulette wheel selection
def select(population):
    max_fitness = sum([fitness(chromo) for chromo in population])
    pick = random.uniform(0, max_fitness)
    current = 0
    for chromo in population:
        current += fitness(chromo)
        if current > pick:
            return chromo

# one-point crossover
def crossover(parent1, parent2):
    point = random.randint(1, nodes - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# mutation
def mutate(chromosome, rate):
    if random.random() < rate:
        point = random.randint(0, nodes - 1)
        chromosome[point] = random.choice(colors)
    return chromosome

# genetic algorithm
def genetic_algorithm():
    population = generate_population(population_size, nodes, colors)
    for generation in range(generations):
        new_population = []
        for _ in range(population_size // 2):
            parent1 = select(population)
            parent2 = select(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1, mutation_rate))
            new_population.append(mutate(child2, mutation_rate))
        population = sorted(population + new_population, key=lambda chromo: fitness(chromo))[:population_size]
        best_fitness = fitness(population[0])
        print(f'Generation {generation + 1}: Best Fitness = {best_fitness}')
        if best_fitness == 0:
            break
    return population[0]

# shows the graph of the task
def show_graph(A):
    print(""
        +"\n|===========+===========+============+"
        +"\n|           |           |            |"
        +"\n|           |           |            |"
        +"\n|  "+A[12]+"  /-----+  "+A[11]+"  /-----+------\  "+A[0]+"  |"
        +"\n| 13  |     | 12  |            |  1  |"
        +"\n|     |     |     |            |     |"
        +"\n|-----+  "+A[10]+"  \-----+  "+A[1]+"  /------+-----+"
        +"\n|     | 11        |  2  |            |"
        +"\n|     |           |     |            |"
        +"\n|  "+A[9]+"  +-----------+-----+      "+A[2]+"     |"
        +"\n| 10  |     "+A[8]+"     |  "+A[3]+"  |      3     |"
        +"\n|     |     9     |  4  |            |"
        +"\n|-----+-----+-----+-----++-----+-----+"
        +"\n|           |            |     |     |"
        +"\n|           |            |     |     |"
        +"\n|     "+A[7]+"     |      "+A[6]+"     |  "+A[5]+"  |  "+A[4]+"  |"
        +"\n|     8     |      7     |  6  |  5  |"
        +"\n|           |            |     |     |"
        +"\n|===========+============+=====+=====+"
        )

# run the algorithm
best_solution = genetic_algorithm()
color_map = {0: 'Blue', 1: 'Red', 2: 'Green', 3: 'Yellow'}
print("\nBest Solution:")
for i in range(nodes):
    print(i+1, color_map[best_solution[i]])

show_graph([A[0] for A in [color_map[color] for color in best_solution]])
