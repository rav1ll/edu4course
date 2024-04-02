import random
import numpy as np


def create_initial_population(population_size, num_cities):
    paths = [random.sample(range(num_cities), num_cities) for _ in range(population_size)]
    return paths


def crossover(parent1, parent2):
    length = len(parent1)
    start, end = sorted(random.sample(range(length), 2))
    offspring = parent1[start:end]

    for city in parent2:
        if city not in offspring:
            offspring.append(city)
    return offspring


def mutate(path, mutation_rate):
    if random.random() < mutation_rate:
        start, end = sorted(random.sample(range(len(path)), 2))
        path[start:end] = reversed(path[start:end])
    return path


def calculate_total_distance(path, distance_matrix):
    path_length = sum(distance_matrix[path[i], path[i + 1]] for i in range(len(path) - 1))
    path_length += distance_matrix[path[-1], path[0]]
    return path_length


def genetic_algorithm(distance_matrix, population_size, num_generations, mutation_rate):
    num_cities = len(distance_matrix)
    population = create_initial_population(population_size, num_cities)

    for generation in range(num_generations):
        fitness_scores = [1 / calculate_total_distance(path, distance_matrix) for path in population]

        fitness_sum = sum(fitness_scores)
        selection_prob = [fitness / fitness_sum for fitness in fitness_scores]
        selected_indices = np.random.choice(range(population_size), size=population_size, p=selection_prob)
        selected_population = [population[i] for i in selected_indices]

        next_generation = []
        for i in range(0, population_size, 2):
            parent1, parent2 = selected_population[i], selected_population[i + 1]
            offspring1, offspring2 = crossover(parent1, parent2), crossover(parent2, parent1)
            next_generation.extend([mutate(offspring1, mutation_rate), mutate(offspring2, mutation_rate)])

        population = next_generation

    best_path = min(population, key=lambda path: calculate_total_distance(path, distance_matrix))
    best_distance = calculate_total_distance(best_path, distance_matrix)
    best_path_cities = [cities[i] for i in best_path]

    return best_path_cities, best_distance


path_lengths = {
    "Moscow":
        {
            "Moscow": 0,
            "Saint Petersburg": 705,
            "Kazan": 815,
            "RnD": 1070,
            "Volgograd": 965,
            "Vladivostok": 9165
        },

    "Saint Petersburg":
        {
            "Moscow": 705,
            "Saint Petersburg": 0,
            "Kazan": 1531,
            "RnD": 1788,
            "Volgograd": 1680,
            "Vladivostok": 9635
        },

    "Kazan":
        {
            "Moscow": 815,
            "Saint Petersburg": 1531,
            "Kazan": 0,
            "RnD": 1505,
            "Volgograd": 1069,
            "Vladivostok": 8334
        },

    "RnD":
        {
            "Moscow": 1070,
            "Saint Petersburg": 1788,
            "Kazan": 1500,
            "RnD": 0,
            "Volgograd": 400,
            "Vladivostok": 9385
        },

    "Volgograd":
        {
            "Moscow": 965,
            "Saint Petersburg": 1680,
            "Kazan": 1069,
            "RnD": 400,
            "Volgograd": 0,
            "Vladivostok": 9060
        },

    "Vladivostok":
        {"Moscow": 9165,
         "Saint Petersburg": 9635,
         "Kazan": 8334,
         "RnD": 9385,
         "Volgograd": 9060,
         "Vladivostok": 0
         },

}

cities = list(path_lengths.keys())
distance_matrix = np.array([[path_lengths[city1][city2] for city2 in cities] for city1 in cities])

size_population = 100
generations = 1000
mutation_rate = 0.01


def main():
    ga = genetic_algorithm(distance_matrix,
                           size_population,
                           generations,
                           mutation_rate)

    print('оптимальный путь: ')
    print(*ga[0], sep=' - ')
    print('суммарное расстояние: ')
    print(ga[1])


if __name__ == "__main__":
    main()
