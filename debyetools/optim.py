from deap import base, creator, tools, algorithms
import numpy as np
import random
from debyetools.ndeb import nDeb


def get_params_list(params, params_alt, lst_str_alt):
    # E0, V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef, vdef, pel0, pel1, pel2, pel3
    lst_str = ['E0', 'V0', 'K0', 'K0p', 'nu', 'a0', 'm0', 's0', 's1', 's2',
               'edef', 'sdef', 'vdef', 'pel0', 'pel1', 'pel2', 'pel3', 'xs0', 'xs1', 'xs2', 'xs3', 'xs4', 'xs5']

    dict_params = dict(zip(lst_str, params))
    dict_params_alt = dict(zip(lst_str_alt, params_alt))
    lst_params = []
    for k in lst_str:
        if k in lst_str_alt:
            lst_params.append(dict_params_alt[k])
        else:
            lst_params.append(dict_params[k])

    return lst_params


def eval_distance(sample, min_distance, mean_distance):
    sorted_sample = np.sort(sample)
    differences = np.diff(sorted_sample)

    if np.mean(differences) <= mean_distance:
        return False
    else:
        if np.min(differences) <= min_distance:
            return False
        else:
            return True


def random_sample_with_min_distance_2d(array, sample_size, min_distance, mean_distance, rec_depth=0):
    # Extract the second row which will be used for comparison
    values_to_sample_from = array[1, :]

    indexes = array[0, :]

    sample = random.sample(list(values_to_sample_from), sample_size)
    index_sample = [np.where(array[1, :] == i)[0][0] for i in sample]
    sorted_ix = np.argsort(sample)
    sample = np.array(sample)[sorted_ix]
    index_sample = np.array(index_sample)[sorted_ix]

    eval_dist = eval_distance(sample, min_distance, mean_distance)

    if eval_dist or rec_depth > 500:

        return np.array([indexes[index_sample], sample])

    else:
        return random_sample_with_min_distance_2d(array, sample_size, min_distance, mean_distance, rec_depth + 1)

def props(T, params, mass,  eos_pot, Tmelting, v=False):
    global time_eos, time_Fmin, time_tprops
    E0, V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef, vdef, pel0, pel1, pel2, pel3, xs0, xs1, xs2, xs3, xs4, xs5 = params

    # print('params:', params)
    p_intanh = np.array([a0, m0])
    p_anh =  np.array([s0, s1, s2])
    p_electronic = np.array([pel0, pel1, pel2, pel3])
    p_defects = np.array([edef, np.sqrt(sdef ** 2), Tmelting, vdef])
    # print('p_defects', p_defects)

    # EOS parametrization
    #=========================
    initial_parameters = [E0, V0, K0, K0p]
    eos_pot.fitEOS([V0], 0, initial_parameters=initial_parameters, fit=False)
    p_EOS = eos_pot.pEOS
    #=========================

    # F minimization
    #=========================
    ndeb_MU = nDeb(nu, mass, p_intanh, eos_pot, p_electronic, p_defects, p_anh, mode='jjsl',
                   xsparams=[xs0, xs1, xs2, xs3, xs4, xs5], r=1)
    # ndeb_MU.r = 4
    T, V = ndeb_MU.min_G(T, p_EOS[1], P=0)
    # print(f'T: [{T[0]:.2f} ... {T[-1]:.2f}]')
    # print(f'V: [{V[0]:.2e} ... {V[-1]:.2e}]')
    #=========================

    # Evaluations
    #=========================
    tprops_dict = ndeb_MU.eval_props(T, V, P=0)

    #=========================
    del V
    return tprops_dict

# Fitness function
# def eval_error(f, pf, Xdata, Ydata, norm_factor):
#     pfdenorm = [pfi*nfi for nfi, pfi in zip(norm_factor, pf)]
#     Ymodel = f(Xdata, pfdenorm)
#     return np.sqrt(np.mean(((Ydata - Ymodel)/Xdata)**2)),


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


import random
import numpy as np


# Step 1: Define fitness function
def eval_error(f, individual, Xdata, Ydata, norm_factor):
    # Denormalize parameters
    denorm_individual = [param * factor for param, factor in zip(individual, norm_factor)]
    # Calculate the error as fitness (e.g., mean squared error between predicted and actual Y)
    predictions = f(Xdata, denorm_individual)
    mse = np.mean((Ydata - predictions) ** 2)
    return mse


# Step 2: Initialize population
def initialize_population(npop, n_params, plimdn, plimup):
    population = [[random.uniform(plimdn, plimup) for _ in range(n_params)] for _ in range(npop)]
    return population


# Step 3: Selection (Tournament Selection)
def tournament_selection(population, fitnesses, tournsize=3):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, fitnesses)), tournsize)
        selected.append(min(tournament, key=lambda x: x[1])[0])  # Minimize fitness
    return selected


# Step 4: Crossover (Blend Crossover)
def blend_crossover(parent1, parent2, alpha=0.5):
    return [(alpha * p1 + (1 - alpha) * p2) for p1, p2 in zip(parent1, parent2)]


# Step 5: Mutation (Bounded Mutation)
def bounded_mutate(individual, low, up, pmut):
    return [random.uniform(low, up) if random.random() < pmut else gene for gene in individual]


# Step 6: Genetic Algorithm Main Function
def ga_fitting(f, Xdata, Ydata, initial_guess, param_range=(0.8, 1.2), npop=20, ngen=100, tol=1e-6,
               pcross=0.5, pmut=0.2, stagnant_gens=20, verbose=True):
    norm_factor = initial_guess
    plimdn, plimup = param_range
    n_params = len(initial_guess)

    # Initialize population
    population = initialize_population(npop, n_params, plimdn, plimup)

    prev_best = None
    stagnant_count = 0

    best_individual = [1 for _ in range(n_params)]
    if verbose:
        print('Initial fitness:', eval_error(f, best_individual, Xdata, Ydata, norm_factor))

    for gen in range(ngen):
        # Step 1: Evaluate fitness
        population = population + [best_individual]
        fitnesses = [eval_error(f, ind, Xdata, Ydata, norm_factor) for ind in population]

        # Step 2: Check for convergence
        best_fitness = min(fitnesses)
        best_individual = population[fitnesses.index(best_fitness)]
        best_individual_denorm = [p * f for p, f in zip(best_individual, norm_factor)]
        norm_factor = best_individual_denorm

        if verbose:
            print(
                f"Generation {gen}: Best fitness = {best_fitness}, stagnant count: {stagnant_count}")

        if prev_best is not None:
            if abs(best_fitness - prev_best) < tol:

                stagnant_count += 1
            elif abs(best_fitness - prev_best) < tol/10:
                stagnant_count = stagnant_gens
            else:
                stagnant_count = 0
        prev_best = best_fitness

        if stagnant_count >= stagnant_gens:
            if verbose:
                print("Convergence criterion met. Stopping.")
            break

        # Step 3: Selection
        selected = tournament_selection(population, fitnesses)

        # Step 4: Crossover and Mutation
        offspring = []
        while len(offspring) < npop:
            if random.random() < pcross:
                # Perform crossover
                parent1, parent2 = random.sample(selected, 2)
                child = blend_crossover(parent1, parent2)
            else:
                # No crossover, just copy
                child = random.choice(selected)

            # Perform mutation
            child = bounded_mutate(child, plimdn, plimup, pmut)
            offspring.append(child)

        # Replace population with offspring
        population = offspring



    # Return denormalized best individual
    print("Best individual:", best_individual_denorm)
    print("Best fitness:", best_fitness)

    return best_individual_denorm
