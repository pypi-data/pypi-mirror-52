'''
@Author: Wenjie Yin, yinwenjie159@hotmail.com
@Date: 2019-07-11 10:59:22
@LastEditors: Wenjie Yin, yinwenjie159@hotmail.com
@LastEditTime: 2019-07-12 14:40:53
@Description: Autoencoder
'''

import os
import torch
from torchvision import models
from torch import nn
from torch.autograd import Variable

from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torchvision import transforms as tfs
from torchvision.utils import save_image

im_tfs = tfs.Compose([
    tfs.ToTensor(),
    tfs.Normalize([0.5], [0.5])
])

train_set = MNIST('./data/mnist', transform=im_tfs, download=True)
train_data = DataLoader(train_set, batch_size=128, shuffle=True)

net = models.resnet50(pretrained=True)

class autoencoder(nn.Module):
    def __init__(self):
        super(autoencoder, self).__init__()

        self.encoder = nn.Sequential(
            nn.Linear(28*28, 128),
            nn.ReLU(True),
            nn.Linear(128, 64),
            nn.ReLU(True),
            nn.Linear(64, 12),
            nn.ReLU(True),
            nn.Linear(12, 3)
        )

        self.decoder = nn.Sequential(
            nn.Linear(3, 12),
            nn.ReLU(True),
            nn.Linear(12, 64),
            nn.ReLU(True),
            nn.Linear(64, 128),
            nn.ReLU(True),
            nn.Linear(128, 28*28),
            nn.Tanh()
        )

    def forward(self, x):
        encode = self.encoder(x)
        decode = self.decoder(encode)

        return encode, decode
        
net = autoencoder().cuda(0)
criterion = nn.MSELoss(reduction='sum')
optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)

def to_img(x):
    x = 0.5 * (x + 1.)
    x = x.clamp(0, 1)
    x = x.view(x.shape[0], 1, 28, 28)
    return x

for e in range(100):
    for im, _ in train_data:
        im = im.cuda(0)
        im = im.view(im.shape[0], -1)
        im = Variable(im)

        _, output = net(im)
        loss = criterion(output, im) / im.shape[0]

        optimizer.zero_grad() 
        loss.backward()
        optimizer.step()
    
    if (e+1) % 5 == 0:
        print('epoch:{}, loss:{:.4f}'.format(e+1, loss.item()))
        pic = to_img(output.cpu().data)
        if not os.path.exists('./img'):
            os.mkdir('./img')
        save_image(pic, './img/img_{}.png'.format(e+1))
