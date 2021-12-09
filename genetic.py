import random
from functools import reduce


def reproduce(generation):
    next_generation = []

    while len(generation) > 1:
        individual = generation.pop()

        best_candidate_diff = -1
        best_candidate = -1

        for candidate in generation:
            candidate_diff = 0
            for i in range(x_count):
                candidate_diff += abs(individual[i] - candidate[i])

            if candidate_diff > best_candidate_diff:
                best_candidate_diff = candidate_diff
                best_candidate = candidate

        generation.remove(best_candidate)

        child_count = random.randint(2, 4)
        for i in range(child_count):
            child = get_child(individual, best_candidate)
            next_generation.append(child)

    return next_generation


def start(generation_values_range=[1, 25],
          generation_size=5):
    individuals = []

    for i in range(generation_size):
        individual = [random.randint(*generation_values_range) for _ in range(x_count)]
        individuals.append(individual)

    return individuals


def get_child(parent1, parent2):
    temp_array = [parent1, parent2]
    child = []

    for i in range(x_count):
        child.append(temp_array[random.randint(0, 1)][i])

    return child


def mutate(generation):
    for individual in generation:
        for i in range(x_count):
            individual[i] += random.randint(-2, 2)


def target_fn(params, individual):
    return sum([params[i] * individual[i] for i in range(x_count)])


def selection(generation, params, result, limit=4):
    sorted_by_fn = sorted(generation, key=lambda individual: abs(result - target_fn(params, individual)))
    return sorted_by_fn[:limit]


if __name__ == '__main__':
    x_count = 6
    param_value_range = [0, 15]
    param_values = [random.randint(*param_value_range) for x in range(x_count)]

    solution_x_value_range = [0, 10]
    possible_x_values = [random.randint(*solution_x_value_range) for x in range(x_count)]

    result = target_fn(param_values, possible_x_values)

    print("уравнение: " + reduce(lambda x, y: x + " + " + y,
                 [str(param_values[i]) + " * x" + str(i) for i in range(x_count)]) + " = " + str(result))

    solution = None
    generation_limit = 1000
    generation_number = 0

    current = start()

    while True:
        current = reproduce(current)
        mutate(current)
        current = selection(current, param_values, result)

        if target_fn(param_values, current[0]) == result:
            solution = current[0]
            break

        generation_number += 1
        if generation_number > generation_limit:
            break

    print('итог: ', solution)
    print('количество поколений: ', generation_number)
    print('последнее поколение: ', current)
