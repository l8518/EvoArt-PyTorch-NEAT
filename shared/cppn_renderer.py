from time import time
import os
import torch
import torchvision
import io
import random

class CppnRenderer(object):
    def __init__(self):
        self.frames = [open(os.path.join("img_output", "initial_{0}_results_image.png".format(f)), 'rb').read() for f in
                       range(20)]
        self.t = 0.0

    def get_frame(self, cppn, x_dim=250, y_dim=250, current_itensity_band= []):
        """
        Renders an image from a cppn output node and returns PIL image.
        :param cppn_output_node: cppn's output node
        :param x_dim: X Dimension for image, Defaults to 250
        :param y_dim: Y Dimension for image, Defaults to 250
        :return: A PIL image.
        """
        self.t = self.t + 1.0
        tune = 10

        y_px_list = [[i for i in range(y_dim)] for j in range(y_dim)]
        x_px_list = [[i for j in range(x_dim)] for i in range(x_dim)]
        r_px_list = [[1 for j in range(x_dim)] for i in range(x_dim)]
        g_px_list = [[2 for j in range(x_dim)] for i in range(x_dim)]
        b_px_list = [[3 for j in range(x_dim)] for i in range(x_dim)]

        f0_px_list = [[current_itensity_band[0] * tune for j in range(x_dim)] for i in range(x_dim)]
        f1_px_list = [[current_itensity_band[1] * tune for j in range(x_dim)] for i in range(x_dim)]

        r_tensor = cppn(x_in=torch.tensor(x_px_list, dtype=torch.float32),
                        y_in=torch.tensor(y_px_list, dtype=torch.float32),
                        rgb_in=torch.tensor(r_px_list, dtype=torch.float32),
                        f_0=torch.tensor(f0_px_list, dtype=torch.float32),
                        f_1=torch.tensor(f1_px_list, dtype=torch.float32),
                        )
        g_tensor = cppn(x_in=torch.tensor(x_px_list, dtype=torch.float32),
                        y_in=torch.tensor(y_px_list, dtype=torch.float32),
                        rgb_in=torch.tensor(g_px_list, dtype=torch.float32),
                        f_0=torch.tensor(f0_px_list, dtype=torch.float32),
                        f_1=torch.tensor(f1_px_list, dtype=torch.float32),
                        )
        b_tensor = cppn(x_in=torch.tensor(x_px_list, dtype=torch.float32),
                        y_in=torch.tensor(y_px_list, dtype=torch.float32),
                        rgb_in=torch.tensor(b_px_list, dtype=torch.float32),
                        f_0=torch.tensor(f0_px_list, dtype=torch.float32),
                        f_1=torch.tensor(f1_px_list, dtype=torch.float32),
                        )
        rgb_tensor = torch.stack([r_tensor, g_tensor, b_tensor], 0)

        pil_img = torchvision.transforms.ToPILImage()(rgb_tensor)
        imgByteArr = io.BytesIO()
        pil_img.save(imgByteArr, format='PNG')
        imgByteArr = imgByteArr.getvalue()
        return imgByteArr
