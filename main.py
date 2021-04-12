from evolution import evolution, Selection
import matplotlib.pyplot as plt
import math


def plot(data, title='Title'):
    data_to_plot = [[], []]

    for population in data:
        for agent in population['population']:
            for i, parameter in enumerate(agent['parameters']):
                if i == 0:
                    data_to_plot[0].append(parameter)
                else:
                    data_to_plot[1].append(parameter)

    fig, ax = plt.subplots()
    ax.scatter(data_to_plot[0], data_to_plot[1], s=5)

    ax.set_xlabel('x', fontsize=15)
    ax.set_ylabel('y', fontsize=15)
    ax.set_title(title)

    plt.show()
    

def avg_value(population):
    avg = []

    for i in range(len(population[0]['parameters'])):
        values_sum = 0
        for agent in population:
            values_sum += agent['parameters'][i]
        avg.append(round(values_sum / len(population), 2))
    return avg


def test_1():
    func = lambda x, y: 1/(x**2 + y**2 + 1)
    population_size = 20
    num_of_generations = 800
    starting_parameters = [5, 5]
    mutation_probability = 0.1
    mutation_sigma = 0.2

    for selection_type in Selection:
        data = evolution(
            population_size,
            num_of_generations,
            starting_parameters,
            func,
            mutation_probability,
            mutation_sigma,
            selection_type
        )
        plot(data, f'{selection_type.name} selection'.lower())
        last_population = data[-1]['population']
        print(f'{selection_type.name} selection: {avg_value(last_population)}')


def test_2():
    func = lambda a, b, c, d: 1/((a+2)**2 + (b-5)**2 + (c+3)**4 + d**2 + 1)
    population_size = 20
    num_of_generations = 500
    starting_parameters = [0, 0, 0, 0]
    mutation_probability = 0.1
    mutation_sigma = 0.2

    for selection_type in Selection:
        print(f'{selection_type.name} selection:')
        for num_of_generations in [200, 600, 1000]:
            data = evolution(
                population_size,
                num_of_generations,
                starting_parameters,
                func,
                mutation_probability,
                mutation_sigma,
                selection_type
            )
            last_population = data[-1]['population']
            print(f'{num_of_generations} generations: {avg_value(last_population)}')
        print()


def test_3():
    func = lambda x, y: 1/(x**2 + y**2 + 1)
    population_size = 20
    num_of_generations = 800
    starting_parameters = [5, 5]
    mutation_probability = 0.1

    for selection_type in Selection:
        print(f'{selection_type.name} selection:')
        for mutation_sigma in [0.05, 0.2, 1]:
            data = evolution(
                population_size,
                num_of_generations,
                starting_parameters,
                func,
                mutation_probability,
                mutation_sigma,
                selection_type
            )
            plot(data, f'{selection_type.name} selection | sigma = {mutation_sigma}'.lower())
            last_population = data[-1]['population']
            print(f'sigma = {mutation_sigma}: {avg_value(last_population)}')
        print()


def main():
    test_1()
    test_2()
    test_3()


if __name__ == "__main__":
    main()