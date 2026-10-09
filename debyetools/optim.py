import numpy as np
import random
import warnings
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

def props(T, params, mass,  eos_pot, Tmelting, v=False, mode='jjsl'):
    """
    Thermodynamic properties for a parameter vector (used as model function in GA fits).

    min_G may return fewer temperatures than requested if the state becomes mechanically unstable
    (see nDeb.min_G); ga_fitting then treats the individual as invalid (fitness = inf).
    """
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
    ndeb_MU = nDeb(nu, mass, p_intanh, eos_pot, p_electronic, p_defects, p_anh, mode=mode,
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

# Step 1: Define fitness function
def _mse(f, params, Xdata, Ydata):
    """Mean squared error of f(Xdata, params) vs Ydata; inf if f fails, returns a different length or a non-finite value."""
    try:
        with np.errstate(all='ignore'):
            predictions = np.asarray(f(Xdata, params), dtype=float)
            Ydata = np.asarray(Ydata, dtype=float)
            if predictions.shape != Ydata.shape:
                return np.inf
            mse = float(np.mean((Ydata - predictions) ** 2))
    except Exception:
        return np.inf
    return mse if np.isfinite(mse) else np.inf


def eval_error(f, individual, Xdata, Ydata, norm_factor):
    """
    Fitness (mean squared error) of a normalised individual, parameters = individual * norm_factor.
    Failed or non-finite evaluations give inf.
    """
    denorm_individual = [param * factor for param, factor in zip(individual, norm_factor)]
    return _mse(f, denorm_individual, Xdata, Ydata)


# Step 2: Initialize population
def initialize_population(npop, n_params, plimdn, plimup, rng=random):
    population = [[rng.uniform(plimdn, plimup) for _ in range(n_params)] for _ in range(npop)]
    return population


# Step 3: Selection (Tournament Selection)
def tournament_selection(population, fitnesses, tournsize=3, rng=random):
    selected = []
    for _ in range(len(population)):
        tournament = rng.sample(list(zip(population, fitnesses)), tournsize)
        selected.append(min(tournament, key=lambda x: x[1])[0])  # Minimize fitness
    return selected


# Step 4: Crossover (Blend Crossover)
def blend_crossover(parent1, parent2, alpha=0.5):
    return [(alpha * p1 + (1 - alpha) * p2) for p1, p2 in zip(parent1, parent2)]


# Step 5: Mutation (Bounded Mutation)
def bounded_mutate(individual, low, up, pmut, rng=random):
    return [rng.uniform(low, up) if rng.random() < pmut else gene for gene in individual]


# Step 6: Genetic Algorithm Main Function
def ga_fitting(f, Xdata, Ydata, initial_guess, param_range=(0.8, 1.2), npop=20, ngen=100, tol=1e-6,
               pcross=0.5, pmut=0.2, stagnant_gens=20, verbose=True, seed=None, zero_scale=None):
    """
    Genetic-algorithm fit of f(Xdata, params) to Ydata (minimises the mean squared error).

    Each individual is a vector of genes g drawn from param_range around the current best
    parameters c (the window moves to the best individual after every generation):
    p_i = c_i * g_i for parameters whose initial guess is non-zero (relative window; such a
    parameter keeps its sign), and p_i = c_i + zero_scale_i * (g_i - 1) for parameters whose
    initial guess is 0 (absolute window of fixed width; can move away from 0 and change sign).
    Without zero_scale, parameters with initial guess 0 stay at 0 (a UserWarning is issued).

    The best individual is always kept (elitism), so the best fitness never increases.
    Evaluations that raise, return a different length or a non-finite value get fitness = inf.

    :param callable f: model, f(Xdata, params) -> predictions with the shape of Ydata.
    :param np.ndarray Xdata: independent variable.
    :param np.ndarray Ydata: data to fit.
    :param list initial_guess: initial parameters.
    :param tuple param_range: (low, up) range of the genes.
    :param int npop: population size.
    :param int ngen: maximum number of generations.
    :param float tol: absolute change of the best fitness below which a generation counts as stagnant.
    :param float pcross: crossover probability.
    :param float pmut: mutation probability per gene.
    :param int stagnant_gens: number of stagnant generations that stops the search.
    :param bool verbose: print progress.
    :param int seed: seed for a private random generator (None: use the global ``random`` module state).
    :param zero_scale: float or sequence; absolute scale for the parameters whose initial guess is 0.
    :return: best parameters.
    :rtype: list
    """
    rng = random.Random(seed) if seed is not None else random
    plimdn, plimup = param_range
    n_params = len(initial_guess)
    center = [float(c) for c in initial_guess]

    additive = [c == 0 for c in center]
    if zero_scale is None:
        zscale = [0.] * n_params
    else:
        zscale = [float(z) for z in np.broadcast_to(np.asarray(zero_scale, dtype=float), (n_params,))]
    if any(a and z == 0 for a, z in zip(additive, zscale)):
        warnings.warn('ga_fitting: parameters with initial guess 0 and no zero_scale stay fixed at 0: indexes %s'
                      % [i for i, (a, z) in enumerate(zip(additive, zscale)) if a and z == 0], UserWarning, stacklevel=2)

    def denorm(ind, c):
        return [ci + zi * (gi - 1.) if ai else ci * gi for gi, ci, ai, zi in zip(ind, c, additive, zscale)]

    def renorm(params, c):
        out = []
        for pi, ci, ai, zi in zip(params, c, additive, zscale):
            if ai:
                out.append((pi - ci) / zi + 1. if zi != 0 else 1.)
            else:
                out.append(pi / ci if ci != 0 else 1.)
        return out

    # Initialize population
    population = initialize_population(npop, n_params, plimdn, plimup, rng=rng)

    prev_best = None
    stagnant_count = 0

    best_individual = [1. for _ in range(n_params)]
    if verbose:
        print('Initial fitness:', _mse(f, denorm(best_individual, center), Xdata, Ydata))

    for gen in range(ngen):
        # Step 1: Evaluate fitness (the elite, a vector of ones in the current normalisation, is always included)
        population = population + [best_individual]
        fitnesses = [_mse(f, denorm(ind, center), Xdata, Ydata) for ind in population]

        # Step 2: Check for convergence
        ibest = int(np.argmin(fitnesses))
        best_fitness = fitnesses[ibest]
        best_params = denorm(population[ibest], center)

        if verbose:
            print(
                f"Generation {gen}: Best fitness = {best_fitness}, stagnant count: {stagnant_count}")

        if prev_best is not None:
            if abs(best_fitness - prev_best) < tol:
                stagnant_count += 1
            else:
                stagnant_count = 0
        prev_best = best_fitness

        if stagnant_count >= stagnant_gens:
            if verbose:
                print("Convergence criterion met. Stopping.")
            break

        # Step 3: Selection
        selected = tournament_selection(population, fitnesses, rng=rng)

        # Step 4: Crossover and Mutation
        offspring = []
        while len(offspring) < npop:
            if rng.random() < pcross:
                # Perform crossover
                parent1, parent2 = rng.sample(selected, 2)
                child = blend_crossover(parent1, parent2)
            else:
                # No crossover, just copy
                child = rng.choice(selected)

            # Perform mutation
            child = bounded_mutate(child, plimdn, plimup, pmut, rng=rng)
            offspring.append(child)

        # Move the window to the best individual and express the offspring in the new normalisation
        new_center = best_params
        population = [renorm(denorm(child, center), new_center) for child in offspring]
        center = new_center
        best_individual = [1. for _ in range(n_params)]

    if verbose:
        print("Best individual:", best_params)
        print("Best fitness:", best_fitness)

    return best_params
