import os
import neat
import numpy as np
import torch
import torchvision

from PIL import Image
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

    # Create population
    pop = neat.Population(config)

    # Determine fitness for each genome.
    def eval_genomes(genomes, config):
        for _, genome in genomes:
            genome.fitness = 1

    # returns winning genome
    generations_n = 1
    genome = pop.run(eval_genomes, generations_n)

    # Create CPPN and unpack to output nodes
    [o1] = create_cppn(
        genome,
        config,
        ["x_in", "y_in", "rgb_in"],
        ["output_node"]
    )

    x_dim = 100
    y_dim = 100
    print ("Define Lambdas")
    fr = lambda x, y: o1(
        x_in=torch.tensor(x, dtype=torch.float32),
        y_in=torch.tensor(y, dtype=torch.float32),
        rgb_in=torch.tensor(1, dtype=torch.float32))

    fg = lambda x, y: o1(
        x_in=torch.tensor(x, dtype=torch.float32),
        y_in=torch.tensor(y, dtype=torch.float32),
        rgb_in=torch.tensor(2, dtype=torch.float32))

    fb = lambda x, y: o1(
        x_in=torch.tensor(x, dtype=torch.float32),
        y_in=torch.tensor(y, dtype=torch.float32),
        rgb_in=torch.tensor(3, dtype=torch.float32))

    print("Query CPPN")
    rval = np.fromfunction(np.vectorize(fr), (x_dim, y_dim), dtype=float)
    gval = np.fromfunction(np.vectorize(fg), (x_dim, y_dim), dtype=float)
    bval = np.fromfunction(np.vectorize(fb), (x_dim, y_dim), dtype=float)

    print("Build PyTorch Tensor")
    matrix = torch.tensor([rval, gval, bval], dtype=torch.float32)

    # Create Random Noise
    print("Build PyTorch Random Tensor")
    imarray = torch.rand(3, x_dim, y_dim)

    print("Interpret CPPN-based PyTorch Tensor as Image")
    results = torchvision.transforms.ToPILImage()(matrix)
    results.save('results_image.png')

    print("Interpret random PyTorch Tensor as Image")
    results_rand = torchvision.transforms.ToPILImage()(imarray)
    results_rand.save('results_rand_image.png')


if __name__ == "__main__":
    run()
