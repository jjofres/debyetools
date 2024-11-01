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

def ga_fitting(f, Xdata, Ydata, initial_guess, param_range=(0.8, 1.2), npop = 20, ngen=100, tol=1e-6,
             pcross=0.5, pmut=0.2, stagnant_gens=20, verbose=True):
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

    if verbose:
        print('Initial fitness:', list(map(toolbox.evaluate, [[1,1]]))[0][0])
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=CXPB, mutpb=MUTPB)
        fits = map(toolbox.evaluate, offspring)

        for fit, ind in zip(fits, offspring):
            # print(f'fitness: {fit[0]:.7f}', 'ind', ind)
            ind.fitness.values = fit

        population = toolbox.select(offspring, k=len(population))

        # Check for convergence
        best_ind = tools.selBest(population, 1)[0]
        best_fitness = round(best_ind.fitness.values[0], 7)
        if verbose:
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