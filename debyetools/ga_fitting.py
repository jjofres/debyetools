from deap import base, creator, tools, algorithms
import numpy as np
import random

# Fitness function
def eval_error(f, pf, Xdata, Ydata, norm_factor):
    pfdenorm = [pfi*nfi for nfi, pfi in zip(norm_factor, pf)]
    Ymodel = f(Xdata, pfdenorm)
    return np.sqrt(np.mean(((Ydata - Ymodel)/Xdata)**2)),


def bounded_mutate(individual, low, up, indpb):
    size = len(individual)
    for i in range(size):
        if random.random() < indpb:
            individual[i] += random.gauss(0, 1)
            if individual[i] < low:
                individual[i] = low
            elif individual[i] > up:
                individual[i] = up
    return individual,

def ga_optim(f, Xdata, Ydata, initial_guess, param_range=(0.8, 1.2), npop = 20, ngen=100, tol=1e-6,
             pcross=0.5, pmut=0.2, stagnant_gens=20):
    norm_factor = initial_guess
    # Define bounds for each parameter
    plimdn, plimup =param_range
    # Genetic Algorithm setup
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("attr_float", random.uniform, plimdn, plimup)  # Parameter range
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=len(initial_guess))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    #toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.register("mutate", bounded_mutate, low=plimdn, up=plimup, indpb=pmut)
    toolbox.register("select", tools.selTournament, tournsize=3)
    evaluate = lambda individual_norm: eval_error(f, individual_norm, Xdata, Ydata, norm_factor)
    toolbox.register("evaluate", evaluate)


    population = toolbox.population(n=npop)  # Initial population
    # population.append(initial_individual)  # Add the initial guess to the population

    NGEN = ngen  # Number of generations
    CXPB, MUTPB = pcross, pmut  # Crossover and mutation probabilities
    tolerance = tol  # Convergence tolerance
    stagnant_generations = stagnant_gens  # Number of generations to check for stagnation
    prev_best = None
    stagnant_count = 0
    # Evolutionary process
    for gen in range(NGEN):
        print('gen:', gen)
        offspring = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)
        fits = map(toolbox.evaluate, offspring)

        for fit, ind in zip(fits, offspring):
            print(f'fitness: {fit[0]:.7f}', 'ind', ind)
            ind.fitness.values = fit

        population = toolbox.select(offspring, k=len(population))

        # Check for convergence
        best_ind = tools.selBest(population, 1)[0]
        best_fitness = round(best_ind.fitness.values[0], 7)
        print(f"Generation {gen}: Best fitness = {best_fitness}, stagnant count:{stagnant_count}")

        if prev_best is not None:
            if abs(best_fitness - prev_best) < tolerance:
                stagnant_count += 1
            else:
                stagnant_count = 0

        prev_best = best_fitness

        if stagnant_count >= stagnant_generations:
            print("Convergence criterion met (stagnant_count). Stopping.")
            break

    best_ind = tools.selBest(population, 1)[0]
    print('Best individual:', best_ind)
    print('Fitness:', best_ind.fitness.values)

    return [pfi*nfi for nfi, pfi in zip(norm_factor, best_ind)]