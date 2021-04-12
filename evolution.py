import random
from enum import Enum


class Selection(Enum):
    ROULETTE = 0
    TOURNAMENT = 1
    THRESHOLD = 2


class Agent:

    def __init__(self, parameters):
        self.parameters = parameters

    def randomize(self, sigma=1):
        self.parameters = [random.gauss(parameter, sigma)
            for parameter in self.parameters]
        return self

    def assess(self, func):
        return func(*self.parameters)


def evolution(population_size, num_of_generations, starting_point,
    objective_func, mutation_probability, sigma, selection_type):
    data = []
    population = initialization(population_size, starting_point, sigma=0.2)

    for i in range(num_of_generations):
        chosen_population = selection(selection_type ,population, objective_func)
        population = breed(chosen_population, mutation_probability, sigma)
        add_data(data, population)

    return data


def initialization(population_size, starting_point, sigma=0.5):
    return [Agent(starting_point).randomize(sigma) for i in range(population_size)]


def selection(selection_type, population, objective_func):
    if selection_type == Selection.ROULETTE:
        return roulette_selection(population, objective_func)
    if selection_type == Selection.TOURNAMENT:
        return tournament_selection(population, objective_func)
    if selection_type == Selection.THRESHOLD:
        return threshold_selection(population, objective_func)


def roulette_selection(population, func):
    values_sum = 0
    agents_weights = []

    for agent in population:
        values_sum += agent.assess(func)

    for agent in population:
        agents_weights.append(agent.assess(func) / values_sum)

    selected_population = random.choices(
        population, weights=agents_weights, k=len(population)//2)
    return selected_population


def tournament_selection(population, func):
    selected_population = []

    while len(selected_population) < len(population) // 2:
        group = random.choices(population, k=2)
        if group[0].assess(func) > group[1].assess(func):
            selected_population.append(group[0])
        else:
            selected_population.append(group[1])

    return selected_population


def threshold_selection(population, func):
    values_sum = 0
    selected_population = []

    for agent in population:
        values_sum += agent.assess(func)

    threshold = round(values_sum / len(population), 6)

    i = 0
    while len(selected_population) < len(population) // 2:
        agent = population[i]
        if round(agent.assess(func), 6) >= round(threshold, 6):
            selected_population.append(agent)

        if i == len(population) - 1:
            i = 0
        else:
            i += 1

    return selected_population


def breed(population, probability, sigma=1): # krzyżowanie jednopunktowe

    def mutation():
        for agent in population:
            if random.random() <= probability:
                agent.randomize(sigma)

    def crossover(agent_1, agent_2):
        cross_point = random.randint(1, len(agent_1.parameters)-1)

        parameters_1 = []
        parameters_2 = []

        for i in range(len(agent_1.parameters)):
            if i <= cross_point:
                parameters_1.append(agent_1.parameters[i])
                parameters_2.append(agent_2.parameters[i])
            else:
                parameters_1.append(agent_2.parameters[i])
                parameters_2.append(agent_1.parameters[i])

        population.append(Agent(parameters_1))
        population.append(Agent(parameters_2))

    mutation()
    for i in range(0, len(population)-1, 2):
        crossover(population[i], population[i+1])

    return population


def add_data(data, population):
    data.append({"population": [agent.__dict__ for agent in population]})


if __name__ == "__main__":
    pass