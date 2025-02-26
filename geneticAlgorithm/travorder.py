# -*- coding: utf-8 -*-
"""travorder.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19GOVnqagKelDNrEhlfMqsxIuFd4ImV5k
"""

import random
import time

# Distances between cities (in kilometers)
distances = {
    ('Boston', 'London'): 3,
    ('London', 'Mumbai'): 4.5,
    ('Mumbai', 'Shanghai'): 3.1,
    ('Shanghai', 'London'): 5.7,
    ('Boston', 'Mumbai'): 7.6,
    ('Boston', 'Shanghai'): 7.8
}

# List of cities (nodes)
cities = ['Boston', 'London', 'Mumbai', 'Shanghai']

# Add self-loop distances (city to itself)
for city in cities:
    distances[(city, city)] = 0.0  # Distance from city to itself is 0

# Step 1: Compute the Route Distance
def calculate_distance(route):
    total_distance = 0.0

    # Calculate the distance from city to city
    for i in range(len(route) - 1):
        forward_distance = distances.get((route[i], route[i+1]))
        reverse_distance = distances.get((route[i+1], route[i]))

        if forward_distance is not None:
            total_distance += forward_distance
        elif reverse_distance is not None:
            total_distance += reverse_distance
        else:
            raise ValueError(f"Distance not found for cities {route[i]} and {route[i+1]}")

    # Ensure the return to the starting city (last city to first city)
    return_distance = distances.get((route[-1], route[0]))
    reverse_return_distance = distances.get((route[0], route[-1]))

    if return_distance is not None:
        total_distance += return_distance
    elif reverse_return_distance is not None:
        total_distance += reverse_return_distance
    else:
        raise ValueError(f"Distance not found for return trip from {route[-1]} to {route[0]}")

    return total_distance

# Test to ensure calculate distance is working correctly

route = ['Boston', 'London', 'Mumbai', 'Shanghai', 'Boston']
distance = calculate_distance(route)
print("Total distance of the route:", distance)
print(route)

# Step 2: Crossover
def crossover(parent1, parent2, crossover_index=None):

    # Ensure the parent routes are not empty
    if not parent1 or not parent2:
        raise ValueError("Parent routes must not be empty.")

    # Ensure both parent routes are closed (first and last cities are the same)
    if parent1[0] != parent1[-1]:
        parent1.append(parent1[0])  # Close parent1 if not closed
    if parent2[0] != parent2[-1]:
        parent2.append(parent2[0])  # Close parent2 if not closed

    # Use the provided crossover index, or select it randomly (if not provided)
    if crossover_index is None:
        crossover_index = random.randint(1, len(parent1) - 2)

    # Taking the first city from parent1 (the child route should start at this city)
    child = [parent1[0]]

    # Add cities from parent1 up to the crossover point
    for i in range(1, crossover_index + 1):
        child.append(parent1[i])

    # Add cities from parent2, skipping cities that are already in the child
    for city in parent2:
        if city not in child:  # Only add cities that are not already in the child
            child.append(city)

    # Ensure the child ends at the same city it starts with
    child.append(child[0])

    return child

# Test crossover is working correctly (and closing the loop)
parent1 = ['Boston', 'London', 'Mumbai', 'Shanghai', 'Boston']  # Closed route 1
parent2 = ['London', 'Mumbai', 'Shanghai', 'Boston', 'London']  # Closed route 2

# Call with the crossover index
child = crossover(parent1, parent2, crossover_index=2)
print("Child Route:", child)

# Step 3: Mutation Function (Swap two random cities)
def mutate(route):
    i, j = random.sample(range(len(route)), 2) # Generating two distinct random indicies from the route
    route[i], route[j] = route[j], route[i] # Swap the position of the two random cities in the route

# Test Mutation Function
route = ['Boston', 'London', 'Mumbai', 'Shanghai']

print("Original route:", route)

# Perform mutation
mutate(route)

print("Mutated route:", route)

# Step 4: Fitness Function (Inverse of distance)
def fitness(route):
    return 1 / calculate_distance(route) # Calculating fitness value to ensure optimal routes (low distance, high fitness value)

# Step 5: Tournament Selection
def tournament_selection(population, tournament_size=5):
    tournament = random.sample(population, tournament_size) # Randomly select a subset of the population
    best = min(tournament, key=calculate_distance) # Select the individual with the smallest distance
    return best

# Create an initial population (random routes)
def create_population(size, cities):
    population = [] # Empty list to hold all routes
    for _ in range(size):
        route = random.sample(cities, len(cities)) # Create a random route by shuffling the list of cities
        population.append(route) # Add the random route to the population
    return population

# Step 6: Genetic Algorithm Loop (TravOrder)
def genetic_algorithm(cities, generations=1000, population_size=100, crossover_index=1, mutation_rate=0.1):
    population = create_population(population_size, cities)
    best_route = min(population, key=calculate_distance)
    best_distance = calculate_distance(best_route)

    for generation in range(generations):
        parent1 = tournament_selection(population)
        parent2 = tournament_selection(population)

        # Crossover
        child = crossover(parent1, parent2, crossover_index)

        # Mutation
        if random.random() < mutation_rate:
            mutate(child)

        # Evaluate child's fitness
        child_distance = calculate_distance(child)
        if child_distance < best_distance:
            best_route = child
            best_distance = child_distance

        # Replace the population with the new population
        population.append(child)
        population.sort(key=calculate_distance)
        population = population[:population_size]  # Keep population size constant

    return best_route

# Running the Genetic Algorithm (TravOrder)
best_route = genetic_algorithm(cities, generations=1000, population_size=100,crossover_index=2, mutation_rate=0.1)
print("Best Route:", best_route)
print("Best Distance:", calculate_distance(best_route))

# TravOrder results for comparison

start_time = time.time()
end_time = time.time()

print(f"Best Route (TravOrder): {best_route}")
print(f"Best Distance (TravOrder): {calculate_distance(best_route)}")
print(f"Execution Time (TravOrder): {end_time - start_time} seconds")

# Testing TravOrder on my data

distances = {
    ('Boston', 'New York'): 2,
    ('New York', 'Tampa'): 5.5,
    ('Tampa', 'Orlando'): 1.1,
    ('Orlando', 'New York'): 6.8,
    ('Boston', 'Tampa'): 7.7,
    ('Boston', 'Orlando'): 7.2
}

# List of cities (nodes)
my_cities = ['Boston', 'New York', 'Tampa', 'Orlando']

# Add self-loop distances (city to itself)
for city in my_cities:
    distances[(city, city)] = 0.0  # Distance from city to itself is 0

# Running the Genetic Algorithm (TravOrder) on my data
best_route = genetic_algorithm(my_cities, generations=1000, population_size=100,crossover_index=2, mutation_rate=0.1)
print("Best Route:", best_route)
print("Best Distance:", calculate_distance(best_route))