# -*- coding:utf-8 -*-
"""
Author:
    Wenjie Yin, yinw@kth.se
"""

import torch.nn as nn


class AE(nn.Module):
    def __init__(self):
        super(AE, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(21*7, 64),
            nn.ReLU(True),
            nn.Linear(64, 16),
        )

        self.decoder = nn.Sequential(
            nn.Linear(16, 64),
            nn.ReLU(True),
            nn.Linear(64, 13*7),
            nn.Tanh(),
        )

    def forward(self, x):
        """
        Note: image dimension conversion will be handled by external methods
        """
        out = self.encoder(x)
        out = self.decoder(out)
        return out
