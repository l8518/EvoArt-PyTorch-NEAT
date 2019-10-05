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

    x_dim = 258
    y_dim = 258

    print("Query CPPN")
    y_px_list = [[i for i in range(y_dim)] for j in range(y_dim)]
    x_px_list = [[i for j in range(x_dim)] for i in range(x_dim)]
    r_px_list = [[1 for j in range(x_dim)] for i in range(x_dim)]
    g_px_list = [[2 for j in range(x_dim)] for i in range(x_dim)]
    b_px_list = [[3 for j in range(x_dim)] for i in range(x_dim)]

    r_tensor = o1(x_in=torch.tensor(x_px_list, dtype=torch.float32), y_in=torch.tensor(y_px_list, dtype=torch.float32),
                  rgb_in=torch.tensor(r_px_list, dtype=torch.float32))
    g_tensor = o1(x_in=torch.tensor(x_px_list, dtype=torch.float32), y_in=torch.tensor(y_px_list, dtype=torch.float32),
                  rgb_in=torch.tensor(g_px_list, dtype=torch.float32))
    b_tensor = o1(x_in=torch.tensor(x_px_list, dtype=torch.float32), y_in=torch.tensor(y_px_list, dtype=torch.float32),
                  rgb_in=torch.tensor(b_px_list, dtype=torch.float32))
    rgb_tensor = torch.stack([r_tensor, g_tensor, b_tensor], 0)

    print("Interpret CPPN-based PyTorch Tensor as Image")
    results = torchvision.transforms.ToPILImage()(rgb_tensor)
    results.save('results_image.png')


if __name__ == "__main__":
    run()
