import torch
from torch import nn
import numpy as np

conv = nn.Conv3d(1, 1, 3)
kernel = np.array([\
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]], \
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]], \
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]]])
kernel = kernel.reshape((1, 1, 3, 3, 3))

conv.weight.data = torch.from_numpy(kernel)