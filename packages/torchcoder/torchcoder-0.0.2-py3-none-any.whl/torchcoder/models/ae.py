# '''
# @Author: Wenjie Yin, yinwenjie159@hotmail.com
# @Date: 2019-07-11 10:59:22
# @LastEditors: Wenjie Yin, yinwenjie159@hotmail.com
# @LastEditTime: 2019-07-27 01:54:09
# @Description: Autoencoder
# '''

# import torch
# from torch import nn
# from torch.autograd import Variable
# from torch.nn import Module
# from torch._jit_internal import weak_module, weak_script_method


# class residual_block(nn.Module):
#     def __init__(self, in_channel, out_channel, same_shape=True):
#         super(residual_block, self).__init__()
#         self.same_shape = same_shape
#         stride = 1 if self.same_shape else 2

#         self.conv1 = conv3x3(in_channel, out_channel, stride=stride)
#         self.bn1 = nn.BatchNorm2d(out_channel)

#         self.conv2 = conv3x3(out_channel, out_channel)
#         self.bn2 = nn.BatchNorm2d(out_channel)
#         if not self.same_shape:
#             self.conv3 = nn.Conv2d(in_channel, out_channel, 1, stride=stride)

#     def forward(self, x):
#         out = self.conv1(x)
#         out = F.relu(self.bn1(out), True)
#         out = self.conv2(out)
#         out = F.relu(self.bn2(out), True)

#         if not self.same_shape:
#             x = self.conv3(x)
#         return F.relu(x+out, True)


# class Encoder_Block(nn.Module):
#     def __init__(self, source_seq_len, hidden_units=(128, 64, 12, 3)):
#         super(Encoder_Block, self).__init__()
#         self.source_seq_len = source_seq_len
#         self.hidden_units = hidden_units
#         # self._layer_num =
#         if self.layer_num == 0:
#             raise ValueError("The size of hidden units must > 0.")
#         self.l1 = nn.Sequential(
#             nn.Linear(self.source_seq_len, self.hidden_units[0]),
#             nn.ReLU(True)
#         )

#         # for i in range(1, self.layer_num):
#         # encoder.append

#     def forward(self, x):
#         # encoder = []
#         out = self.l1(x)

#         # for i in range(1, self.layer_num):
#         #     encoder.append(nn.ReLU(True))
#         #     encoder.append(nn.Linear(self.hidden_units[i-1], \
#         # self.hidden_units[i]))

#         return out

#     @property
#     def layer_num(self):
#         return len(self.hidden_units)


# class AE(nn.Module):
#     def __init__(
#         self,
#         source_seq_len,
#         target_seq_len,
#         hidden_units=(128, 64, 12, 3)):
#         super(AE, self).__init__()
#         self.source_seq_len = source_seq_len
#         self.target_seq_len = target_seq_len
#         self.hidden_units = hidden_units
#         self._layer_num = 0
#         self._encoder = None
#         self._decoder = None
#         self._model = None
#         if self.layer_num == 0:
#             raise ValueError("hidden_layer must > 0")

#     @property
#     def layer_num(self):
#         return len(self.hidden_units)

#     @property
#     def encoder(self):
#         encoder = []
#         encoder.append(nn.Linear(self.source_seq_len, self.hidden_units[0]))
#         for i in range(1, self.layer_num):
#             encoder.append(nn.ReLU(True))
#             encoder.append(
#                 nn.Linear(self.hidden_units[i-1], self.hidden_units[i]))

#         return nn.Sequential(*encoder)

#     @property
#     def decoder(self):
#         decoder = []
#         for i in range(1, self.layer_num):
#             decoder.append(nn.Linear(
#                 self.hidden_units[self.layer_num-i],
#                 self.hidden_units[self.layer_num-i-1]))
#             decoder.append(nn.ReLU(True))
#         decoder.append(nn.Linear(self.hidden_units[0], self.target_seq_len))
#         decoder.append(nn.Tanh())

#         return nn.Sequential(*decoder)

#     @property
#     def model(self):
#         return nn.Sequential(*self.encoder, *self.decoder)


# ae = AE(10, 10)

# print(ae.layer_num)
# print(ae.model)

# print(ae.encoder)
# print(ae.decoder)

# # print(a.children())
