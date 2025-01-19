import numpy as np

class ABC:
    def __init__(self, MCN, nvar, SN, Ub = None, Lb = None,  epsilon = None):
        self.MCN = MCN
        self.nvar = nvar
        self.SN = SN
        self.Ub = Ub
        self.Lb = Lb
        self.epsilon = epsilon

    def fobjective(self, M):
        x1, x2, x3, x4 = M
        SVR = 0
        if self.epsilon is None:
            pass
        else:
            g1 = -x4 + x3 - 0.55
            g2 = -x3 + x4 - 0.55
            h3 = 1000 * np.sin(-x3 - 0.25) + 1000 * np.sin(-x4 - 0.25) + 894.8 - x1
            h4 = 1000 * np.sin(x3 - 0.25) + 1000 * np.sin(x3 - x4 - 0.25) + 894.8 - x2
            h5 = 1000 * np.sin(x4 - 0.25) + 1000 * np.sin(x4 - x3 - 0.25) + 1294.8
            if g1 > 0:
                SVR += g1
            if g2 > 0:
                SVR += g2
            if abs(h3) > self.epsilon:
                SVR += abs(h3)
            if abs(h4) > self.epsilon:
                SVR += abs(h4)
            if abs(h5) > self.epsilon:
                SVR += abs(h5)
        g05 = 3 * x1 + (0.000001) * x1**3 + 2 * x2 + (0.000002 / 3) * x2**3
        return g05, SVR

    def generate_first_source(self):
        if self.Ub is None or self.Lb is None:
            return np.random.uniform(-1000, 1000, (self.SN, self.nvar))
        else:
            return np.random.uniform(self.Lb, self.Ub, (self.SN, self.nvar))

    def evaluate(self, source):
        return np.array([self.fobjective(M) for M in source])
    
    def best_fitness_index(self, fitness, opt = 'max'):
        if self.epsilon is None:
            if opt == 'min':
                return np.argmin(fitness[:, 0])
            else:
                return np.argmax(fitness[:, 0])
        else:
            if np.mean(fitness[:, 1]) == 0:
                if opt == 'min':
                    return np.argmin(fitness[:, 0])
                else:
                    return np.argmax(fitness[:, 0])
            else:
                if opt == 'min':
                    aux = 999999999999
                    #verificar si existe un valor de fitness[:, 1] = 0
                    zeros = np.count_nonzero(fitness[:, 1] == 0)
                    if zeros == 0 or zeros == 1:
                        return np.argmin(fitness[:, 1])
                    else:
                        for i in range(len(fitness[:, 0])):
                            if fitness[i, 1] == 0:
                                if fitness[i, 0] < aux:
                                    aux = fitness[i, 0]
                                    index = i
                        return index
                else:
                    aux = -999999999999
                    #verificar si existe un valor de fitness[:, 1] = 0
                    zeros = np.count_nonzero(fitness[:, 1] == 0)
                    if zeros == 0 or zeros == 1:
                        return np.argmax(fitness[:, 1])
                    else:
                        for i in range(len(fitness[:, 0])):
                            if fitness[i, 1] == 0:
                                if fitness[i, 0] > aux:
                                    aux = fitness[i, 0]
                                    index = i
                        return index
    
    def generate_employer_bee_direction(self):
        M = np.zeros((self.SN, self.nvar + 2))
        for i in range(self.SN):
            j = i
            while j == i:
                j = np.random.randint(self.SN)
            M[i, 0] = i  
            M[i, 1] = j
            M[i, 2:self.nvar + 2] = np.random.rand(self.nvar) * 2 - 1  
        return M

    def flying_bees(self, first_value, second_value, phi):
        return first_value + phi * (first_value - second_value)
    
    def generate_new_source(self, source, bee_direction):
        new_source = np.zeros((self.SN, self.nvar))
        for i in range(self.SN):
            for j in range(self.nvar):
                new_source[i, j] = self.flying_bees(source[int(bee_direction[i, 0]), j], source[int(bee_direction[i, 1]), j], bee_direction[i, j + 2])
        return new_source
    
    def boundaries_correction(self, source):
        for i in range(self.SN):
            for j in range(self.nvar):
                while source[i, j] < self.Lb[j] or source[i, j] > self.Ub[j]:
                    if source[i, j] < self.Lb[j]:
                        source[i, j] = 2 * self.Lb[j] - source[i, j]
                    if source[i, j] > self.Ub[j]:
                        source[i, j] = 2 * self.Ub[j] - source[i, j]
        return source
    
    def get_best_fitness_by_DEB(self, source, new_source, first_fitness, second_fitness, bee_index, limit, opt = 'max'):
        final_fitness = np.copy(first_fitness)
        final_source = np.copy(source)
        if self.epsilon is None:
            if opt == 'max':
                for i in range(self.SN):
                    if first_fitness[int(bee_index[i]), 0] >= second_fitness[i, 0]:
                        limit[int(bee_index[i])] += 1
                        final_fitness[int(bee_index[i]), :] = first_fitness[int(bee_index[i]), :]
                        final_source[int(bee_index[i]), :] = source[int(bee_index[i]), :]
                    else:
                        limit[int(bee_index[i])] = 0
                        final_fitness[int(bee_index[i]), :] = second_fitness[i, :]
                        final_source[int(bee_index[i]), :] = new_source[i, :]
            else:
                for i in range(self.SN):
                    if first_fitness[int(bee_index[i]), 0] <= second_fitness[i, 0]:
                        limit[int(bee_index[i])] += 1
                        final_fitness[int(bee_index[i]), :] = first_fitness[int(bee_index[i]), :]
                        final_source[int(bee_index[i]), :] = source[int(bee_index[i]), :]
                    else:
                        limit[int(bee_index[i])] = 0
                        final_fitness[int(bee_index[i]), :] = second_fitness[i, :]
                        final_source[int(bee_index[i]), :] = new_source[i, :]
        else:
            for i in range(self.SN):
                if first_fitness[int(bee_index[i]), 1] == 0 and second_fitness[i, 1] == 0:
                    if opt == 'max':
                        if first_fitness[int(bee_index[i]), 0] >= second_fitness[i, 0]:
                            limit[int(bee_index[i])] += 1
                            final_fitness[int(bee_index[i]), :] = first_fitness[int(bee_index[i]), :]
                            final_source[int(bee_index[i]), :] = source[int(bee_index[i]), :]
                        else:
                            limit[int(bee_index[i])] = 0
                            final_fitness[int(bee_index[i]), :] = second_fitness[i, :]
                            final_source[int(bee_index[i]), :] = new_source[i, :] 
                    else:
                        if first_fitness[int(bee_index[i]), 0] <= second_fitness[i, 0]:
                            limit[int(bee_index[i])] += 1
                            final_fitness[int(bee_index[i]), :] = first_fitness[int(bee_index[i]), :]
                            final_source[int(bee_index[i]), :] = source[int(bee_index[i]), :]
                        else:
                            limit[int(bee_index[i])] = 0
                            final_fitness[int(bee_index[i]), :] = second_fitness[i, :]
                            final_source[int(bee_index[i]), :] = new_source[i, :]
                elif first_fitness[int(bee_index[i]), 1] == 0 and second_fitness[i, 1] != 0:
                    limit[int(bee_index[i])] += 1
                    final_fitness[int(bee_index[i]), :] = first_fitness[int(bee_index[i]), :]
                    final_source[int(bee_index[i]), :] = source[int(bee_index[i]), :]
                elif first_fitness[int(bee_index[i]), 1] != 0 and second_fitness[i, 1] == 0:
                    limit[int(bee_index[i])] += 0
                    final_fitness[int(bee_index[i]), :] = second_fitness[i, :]
                    final_source[int(bee_index[i]), :] = new_source[i, :]
                else:
                    if first_fitness[int(bee_index[i]), 1] <= second_fitness[i, 1]:
                        limit[int(bee_index[i])] += 1
                        final_fitness[int(bee_index[i]), :] = first_fitness[int(bee_index[i]), :]
                        final_source[int(bee_index[i]), :] = source[int(bee_index[i]), :]
                    else:
                        limit[int(bee_index[i])] = 0
                        final_fitness[int(bee_index[i]), :] = second_fitness[i, :]
                        final_source[int(bee_index[i]), :] = new_source[i, :]

        return final_source, final_fitness


    
    def waggle_dance(self, best_index):
        M = np.zeros((self.SN, self.nvar + 2))
        M[0:int(np.ceil(self.SN/2)), 0] = best_index
        M[int(np.ceil(self.SN/2)):self.SN + 1, 0] = np.random.randint(0, self.SN, int(np.floor(self.SN/2)))
        M[:, 1] = np.random.permutation(self.SN)
        for i in range(self.SN):
            M[i, 2:self.nvar + 2] = np.random.rand(self.nvar) * 2 - 1
        return M

    def scout_bee_phase(self, source, fitness, limit):
        # best_index = self.best_fitness_index(fitness, opt = 'min')
        # best_solution = np.concatenate(np.copy(source[best_index, :]), np.copy(fitness[best_index, :]))
        for i in range(self.SN):
            if self.Ub is None or self.Lb is None:
                if limit[i] >=  self.MCN / 10:
                    source[i, :] = np.random.uniform(-1000, 1000, self.nvar)
                    fitness[i, :] = self.fobjective(source[i, :])
                    limit[i] = 0
            else:
                if limit[i] >= 10 * self.MCN / 10:
                    source[i, :] = np.random.uniform(self.Lb, self.Ub, self.nvar)
                    fitness[i, :] = self.fobjective(source[i, :])
                    limit[i] = 0

        return source, fitness, limit
    

    
    def run(self):
        source = self.generate_first_source()
        limit = np.zeros((self.SN, 1))

        fitness = self.evaluate(source)
        for i in range(self.MCN):
            employer_bee_direction = self.generate_employer_bee_direction()
            new_source = self.generate_new_source(source, employer_bee_direction)
            if self.Ub is not None and self.Lb is not None:
                new_source = self.boundaries_correction(new_source)
            new_fitness = self.evaluate(new_source)
            source, fitness = self.get_best_fitness_by_DEB(source, new_source, fitness, new_fitness, employer_bee_direction[:, 0], limit, opt = 'min') 
            best_index = self.best_fitness_index(fitness, opt = 'min')
            outlooker_bees_waggle_dance = self.waggle_dance(best_index)
            new_source = self.generate_new_source(source, outlooker_bees_waggle_dance)
            if self.Ub is not None and self.Lb is not None:
                new_source = self.boundaries_correction(new_source)
            new_fitness = self.evaluate(new_source)
            source, fitness = self.get_best_fitness_by_DEB(source, new_source, fitness, new_fitness, outlooker_bees_waggle_dance[:, 0], limit, opt = 'min')
            source, fitness, limit = self.scout_bee_phase(source, fitness, limit)
            best_index = self.best_fitness_index(fitness, opt = 'min')
            if i == 0:
                best_solution = source[best_index, :]
            else:
                possible_best_solution = source[best_index, :]
                M = np.zeros((2, self.nvar))
                M[0, :] = best_solution
                M[1, :] = possible_best_solution
                best_solution = M[self.best_fitness_index(self.evaluate(M), opt = 'min'), :]


        print(source)
        print(fitness)
        print(limit)
        print(best_index)
        print(fitness[best_index, :])
        print(best_solution)
        print(self.fobjective(best_solution))

MCN = 5000
nvar = 4
SN = 30
epsilon = 0.001

Ub = np.array([1200, 1200, 0.55, 0.55]) 
Lb = np.array([0, 0, -0.55, -0.55])

# verificar dimensiones
if Ub is None or Lb is None:
    if len(Ub) != nvar or len(Lb) != nvar or len(Ub) != len(Lb):
        print("Boundary dimensions do not match number of variables")
        exit()
    else:
        pass




abc = ABC(MCN, nvar, SN, Ub, Lb, epsilon)
abc.run()






