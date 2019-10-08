import os
import random
import neat
import numpy as np
import torch
import torchvision
import pytorch_neat.cppn

from PIL import Image


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
            genome.fitness = random.randint(1, 200)

    # returns winning genome
    generations_n = 1
    initial_pop = pop.population.values()
    pop.run(eval_genomes, generations_n)

    # Iterate over each genome from last generation save image representation:

    for i, genome in enumerate(pop.population.values()):
        cppn = create_cppn(genome, config)
        prefix = "offspring" # TODO: possibly better done with neat's api - check if initial pop
        if genome in initial_pop:
            prefix = "initial"
        img = render_cppn_as_image(cppn)
        img.save(os.path.join("img_output", "{0}_{1}_results_image.png".format(prefix, i)))


def create_cppn(genome, config):
    """
    Create a CPPN and return it's output node
    :param genome:
    :param config:
    :return:
    """
    # Create CPPN and unpack to output nodes
    [o1] = pytorch_neat.cppn.create_cppn(
        genome,
        config,
        ["x_in", "y_in", "rgb_in"],
        ["output_node"]
    )
    return o1


def render_cppn_as_image(cppn_output_node, x_dim=250, y_dim=250):
    """
    Renders an image from a cppn output node and returns PIL image.
    :param cppn_output_node: cppn's output node
    :param x_dim: X Dimension for image, Defaults to 250
    :param y_dim: Y Dimension for image, Defaults to 250
    :return: A PIL image.
    """

    y_px_list = [[i for i in range(y_dim)] for j in range(y_dim)]
    x_px_list = [[i for j in range(x_dim)] for i in range(x_dim)]
    r_px_list = [[1 for j in range(x_dim)] for i in range(x_dim)]
    g_px_list = [[2 for j in range(x_dim)] for i in range(x_dim)]
    b_px_list = [[3 for j in range(x_dim)] for i in range(x_dim)]

    r_tensor = cppn_output_node(x_in=torch.tensor(x_px_list, dtype=torch.float32),
                                y_in=torch.tensor(y_px_list, dtype=torch.float32),
                  rgb_in=torch.tensor(r_px_list, dtype=torch.float32))
    g_tensor = cppn_output_node(x_in=torch.tensor(x_px_list, dtype=torch.float32),
                                y_in=torch.tensor(y_px_list, dtype=torch.float32),
                  rgb_in=torch.tensor(g_px_list, dtype=torch.float32))
    b_tensor = cppn_output_node(x_in=torch.tensor(x_px_list, dtype=torch.float32),
                                y_in=torch.tensor(y_px_list, dtype=torch.float32),
                  rgb_in=torch.tensor(b_px_list, dtype=torch.float32))
    rgb_tensor = torch.stack([r_tensor, g_tensor, b_tensor], 0)

    pil_img = torchvision.transforms.ToPILImage()(rgb_tensor)
    return pil_img


if __name__ == "__main__":
    run()
