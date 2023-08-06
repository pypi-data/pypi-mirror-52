# -*- coding:utf-8 -*-
"""
Author:
    Wenjie Yin, yinw@kth.se
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

from ..layers import GraphConvolution


class GCNVAE(nn.Module):
    def __init__(self, input_dim, hidden_dim, latent_dim, dropout):
        super(GCNVAE, self).__init__()
        self.gc1 = GraphConvolution(
            input_dim, hidden_dim, dropout, activation=F.relu)
        self.gc2_mu = GraphConvolution(
            hidden_dim, latent_dim, dropout, activation=lambda x: x)
        self.gc2_sig = GraphConvolution(
            hidden_dim, latent_dim, dropout, activation=lambda x: x)
        self.dc = InnerProductDecoder(dropout, activation=lambda x: x)

    def encode(self, x, adj):
        hidden1 = self.gc1(x, adj)
        mu = self.gc2_mu(hidden1, adj)
        log_sig = self.gc2_sig(hidden1, adj)
        return mu, log_sig

    def reparameterize(self, mu, log_sig):
        if self.training:
            std = torch.exp(log_sig)
            eps = torch.randn_like(std)
            return eps.mul(std).add_(mu)
        else:
            return mu

    def forward(self, x, adj):
        mu, log_sig = self.encode(x, adj)
        z = self.reparameterize(mu, log_sig)
        return self.dc(z), mu, log_sig


class InnerProductDecoder(nn.Module):
    """
        Decoder for using inner product for prediction.
    """

    def __init__(self, dropout, activation=torch.sigmoid):
        super(InnerProductDecoder, self).__init__()
        self.dropout = dropout
        self.activation = activation

    def forward(self, z):
        z = F.dropout(z, self.dropout, training=self.training)
        adj = self.activation(torch.mm(z, z.t()))
        return adj
