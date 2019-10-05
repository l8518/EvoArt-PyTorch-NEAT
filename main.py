import os
import neat
import numpy as np
import torch

from pytorch_neat.cppn import create_cppn

def run():

    # Load Python-NEAT config
    config_path = os.path.join(os.path.dirname(__file__), "neat.cfg")
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Create poplulation
    pop = neat.Population(config)

    # Determine fitness for each genome.
    def eval_genomes(genomes, config):
        for _, genome in genomes:
            genome.fitness = 1

    # returns winning genome
    generations_n = 2
    genome = pop.run(eval_genomes, generations_n)

    # Create CPPN and unpack to output nodes
    [o1, o2] = create_cppn(
        genome,
        config,
        ["x_in", "y_in"],
        ["output_node", "output_node"]
    )

    # Define Input
    x_in = torch.tensor(np.array([1.0]))
    y_in = torch.tensor(np.array([2.0]))

    # Query Nodes
    delta_w1 = o1(x_in=x_in, y_in=y_in)
    delta_w2 = o2(x_in=x_in, y_in=y_in)

    print(delta_w1)
    print(delta_w2)


if __name__ == "__main__":
    run()
