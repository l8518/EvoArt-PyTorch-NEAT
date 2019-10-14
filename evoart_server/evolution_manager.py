import os
import neat
import pytorch_neat.cppn


class EvolutionManager(object):
    def __init__(self):
        self.config = None
        self.population = None
        self.load_config()
        self.freq_bands_inputs = self.config.genome_config.num_inputs - 3
        self.init_pop()
        self.generations_n = 0
        self.best_individual = None

    def load_config(self):
        # Load Python-NEAT config
        config_path = os.path.join(os.path.dirname(__file__), "../neat.cfg")
        self.config = neat.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )

    def cppn_input_num(self):
        return

    def get_cppn_freq_bands_inputs(self):
        return self.freq_bands_inputs

    def init_pop(self):
        self.population = neat.Population(self.config)

    def get_individual(self, id):
        return list(self.population.population.values())[id]

    def get_best_individual(self):
        if (self.best_individual is None):
            return self.get_individual(0)
        else:
            return self.best_individual

    def transform_cppn(self, individual):
        # Create CPPN and unpack to output nodes
        [o1] = pytorch_neat.cppn.create_cppn(
            individual,
            self.config,
            ["x_in", "y_in", "rgb_in", *["f_{0}".format(fn) for fn in range(self.freq_bands_inputs)]],
            ["output_node"]
        )
        return o1

    def max_population(self):
        return self.config.pop_size

    def evolve(self, best_individual):
        #     Determine fitness for each genome.
        print(best_individual)
        def eval_genomes(genomes, config):
            y = 0
            for i, genome in genomes:
                y += 1
                if int(y) == int(best_individual):
                    genome.fitness = 10
                else:
                    genome.fitness = 0

        # returns winning genome
        self.generations_n += 1
        genome = self.population.run(eval_genomes, self.generations_n)
        # print(genome)
        self.best_individual = genome
