import torch
import torch.nn as nn
import torch.nn.functional as F


class CrossEntropyLoss(nn.Module):

    def __init__(self, size_average=False):
        """
        Initialization of the cross entropy loss function
        :param size_average: flag that specifies whether to apply size averaging at the end or not
        """

        super(CrossEntropyLoss, self).__init__()

        self.size_average = size_average

    def forward(self, input, target):

        # apply log softmax
        log_p = F.log_softmax(input, dim=1)

        # channels on the last axis
        input_size = input.size()
        for d in range(1, len(input_size) - 1):
            log_p = log_p.transpose(d, d + 1)
        log_p = log_p.contiguous()

        # reshape everything
        log_p = log_p[target[:, 0, ...].unsqueeze(-1).repeat_interleave(input_size[1], dim=-1) >= 0]
        log_p = log_p.view(-1, input_size[1])
        mask = target >= 0
        target = target[mask]

        # compute negative log likelihood
        loss = F.nll_loss(log_p, target)

        # size averaging if necessary
        if self.size_average:
            loss /= mask.data.sum()

        return loss


class MSELoss(nn.Module):

    def forward(self, input, target):
        target_rec = torch.sigmoid(input)
        loss = torch.mean((target - target_rec) ** 2)
        return loss
