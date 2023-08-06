import torch
import torch.nn as nn
import torch.nn.functional as F

from collections import OrderedDict

def _get_padding(kernel_size, stride, dilation):
    padding = ((stride - 1) + dilation * (kernel_size - 1)) // 2
    return padding


class InputConv(nn.Module):
    def __init__(self, inp, outp, k=3, stride=1, dilation=1):
        super(InputConv, self).__init__()
        self.conv = nn.Conv2d(
            inp, outp, k, stride, padding=_get_padding(k, stride, dilation), dilation=dilation)

    def forward(self, x):
        return F.relu6(self.conv(x))


class SeperableConv(nn.Module):
    def __init__(self, inp, outp, k=3, stride=1, dilation=1):
        super(SeperableConv, self).__init__()
        self.depthwise = nn.Conv2d(
            inp, inp, k, stride,
            padding=_get_padding(k, stride, dilation), dilation=dilation, groups=inp)
        self.pointwise = nn.Conv2d(inp, outp, 1, 1)

    def forward(self, x):
        x = F.relu6(self.depthwise(x))
        x = F.relu6(self.pointwise(x))
        return x


class PoseNetwork(nn.Module):

    def __init__(self, output_stride=16):
        super(PoseNetwork, self).__init__()

        self.output_stride = output_stride

        arch = [
            (InputConv, 3, 32, 2),
            (SeperableConv, 32, 64, 1),
            (SeperableConv, 64, 128, 2),
            (SeperableConv, 128, 128, 1),
            (SeperableConv, 128, 256, 2),
            (SeperableConv, 256, 256, 1),
            (SeperableConv, 256, 512, 2),
            (SeperableConv, 512, 512, 1),
            (SeperableConv, 512, 512, 1),
            (SeperableConv, 512, 512, 1),
            (SeperableConv, 512, 512, 1),
            (SeperableConv, 512, 512, 1),
            (SeperableConv, 512, 1024, 2),
            (SeperableConv, 1024, 1024, 1)
        ]

        conv_def = self._to_output_strided_layers(arch, output_stride)
        conv_list = [('conv%d' % c['block_id'], c['conv_type'](
            c['inp'], c['outp'], 3, stride=c['stride'], dilation=c['rate']))
            for c in conv_def]
        last_depth = conv_def[-1]['outp']

        self.features = nn.Sequential(OrderedDict(conv_list))
        self.heatmap = nn.Conv2d(last_depth, 17, 1, 1)
        self.offset = nn.Conv2d(last_depth, 34, 1, 1)
        self.displacement_fwd = nn.Conv2d(last_depth, 32, 1, 1)
        self.displacement_bwd = nn.Conv2d(last_depth, 32, 1, 1)

    def forward(self, x):
        x = self.features(x)
        heatmap = torch.sigmoid(self.heatmap(x))
        offset = self.offset(x)
        displacement_fwd = self.displacement_fwd(x)
        displacement_bwd = self.displacement_bwd(x)
        return heatmap, offset, displacement_fwd, displacement_bwd
    
    def _to_output_strided_layers(self, convolution_def, output_stride):
        current_stride = 1
        rate = 1
        block_id = 0
        buff = []
        for c in convolution_def:
            conv_type = c[0]
            inp = c[1]
            outp = c[2]
            stride = c[3]

            if current_stride == output_stride:
                layer_stride = 1
                layer_rate = rate
                rate *= stride
            else:
                layer_stride = stride
                layer_rate = 1
                current_stride *= stride

            buff.append({
                'block_id': block_id,
                'conv_type': conv_type,
                'inp': inp,
                'outp': outp,
                'stride': layer_stride,
                'rate': layer_rate,
                'output_stride': current_stride
            })
            block_id += 1

        return buff
