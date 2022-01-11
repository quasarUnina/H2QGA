import hqga_utils
import hqga_algorithm
import intervalCode as cod
import copy

def runQGA(device,circuit, params,problem):
    initial_upper_bounds = problem.upper_bounds
    initial_lower_bounds = problem.lower_bounds
    new_upper_bounds = problem.upper_bounds
    new_lower_bounds = problem.lower_bounds
    globalBest=None
    list_bests=[]
    for g in range(params.depth):
        # print(circuit)
        hqga_utils.resetCircuit(circuit)
        problem.upper_bounds = new_upper_bounds
        problem.lower_bounds = new_lower_bounds
        gBest, chromosome_evolution ,bests =hqga_algorithm.runQGA(device, circuit ,params ,problem)
        new_lower_bounds ,new_upper_bounds =cod.convertFromBinToInterval(gBest.chr, problem.lower_bounds, problem.upper_bounds, problem.num_bit_code, problem.dim)
        if params.verbose:
            print(new_lower_bounds ,new_upper_bounds)
        list_bests.append(gBest)
        if globalBest is None:
            globalBest=copy.deepcopy(gBest)
        elif hqga_utils.isBetter(gBest.fitness, globalBest.fitness, problem.isMaxProblem()):
            globalBest=copy.deepcopy(gBest)
    globalBest.chr=str(problem.convert(globalBest.chr))
    problem.upper_bounds = initial_upper_bounds
    problem.lower_bounds = initial_lower_bounds
    return globalBest, list_bests
