from hqga_utils import Parameters
from hqga_utils import ReinforcementParameters
from hqga_utils import ELITISM_R
from hqga_utils import isBetter



class ExtensionsParameters(Parameters):
    def __init__(self, depth, pop_size, max_gen, epsilon_init, prob_mut, elitism, num_shots=1, progressBar=False, verbose=True,draw_circuit=False, qobj_id=None):
            super().__init__(pop_size, max_gen, epsilon_init, prob_mut, elitism, num_shots, progressBar, verbose,
                             draw_circuit, qobj_id)
            self.depth = depth

    def __str__(self):
        return str(self.elitism)+"_depth_"+str(self.depth)+"_eps_init_"+str(self.epsilon_init)+ "_prob_mut_"+str(self.prob_mut)

class ExtensionsReinforcementParameters(ReinforcementParameters):
    def __init__(self, depth, pop_size,max_gen,epsilon_init, epsilon,prob_mut, elitism=ELITISM_R, num_shots=1, progressBar=False, verbose=True,draw_circuit=False,qobj_id=None):
        super().__init__(pop_size,max_gen,epsilon_init, epsilon, prob_mut, elitism, num_shots, progressBar,verbose,draw_circuit, qobj_id)
        self.depth=depth

    def __str__(self):
        return str(self.elitism)+"_depth_"+str(self.depth)+"_eps_init_"+str(self.epsilon_init)+ "_prob_mut_"+str(self.prob_mut)+"_eps_"+str(self.epsilon)



def getOptimum(problem, num_solutions):
        fitnesses=[]
        sols=[]
        if problem.dim==1:
            all_values=getAllValues(problem.lower_bounds[0], problem.upper_bounds[0], num_solutions)
            best=all_values[0]
            best_f=problem.computeFitnessFromReal([all_values[0]])
            for val in all_values:
                chr_real=[val]
                sols.append(val)
                fit=problem.computeFitnessFromReal(chr_real)
                fitnesses.append(fit)
                if (isBetter(fit, best_f,problem.isMaxProblem())):
                    best_f=fit
                    best=val
            best_sols=[]
            best_fits = []
            i=0
            for f in fitnesses:
                if f==best_f:
                    best_sols.append(sols[i])
                    best_fits.append(f)
                i+=1
        if problem.dim == 2:
            all_values=[]
            for i in range(problem.dim):
                all_values.append(getAllValues(problem.lower_bounds[i], problem.upper_bounds[i], num_solutions))
            best = [all_values[0][0],all_values[1][0]]
            best_f = problem.computeFitnessFromReal(best)
            for val1 in all_values[0]:
                for val2 in all_values[1]:
                    chr_real = [val1, val2]
                    sols.append(chr_real)
                    fit = problem.computeFitnessFromReal(chr_real)
                    fitnesses.append(fit)
                    if (isBetter(fit, best_f,problem.isMaxProblem())):
                        best_f = fit
                        best = [val1, val2]
            best_sols = []
            best_fits = []
            i=0
            for f in fitnesses:
                if f==best_f:
                    best_sols.append(sols[i])
                    best_fits.append(f)
                i+=1
        return best_sols, best_fits

def getAllValues(lower_bound, upper_bound,num_solutions):
    list_values = []
    step = (upper_bound - lower_bound) / (num_solutions - 1)
    print("step",step)
    for i in range(num_solutions):
        gene_real = lower_bound + i * step
        list_values.append(gene_real)
    return list_values