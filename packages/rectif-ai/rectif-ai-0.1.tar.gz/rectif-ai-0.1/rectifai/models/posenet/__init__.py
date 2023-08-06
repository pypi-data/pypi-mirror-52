import torch
import os
from rectifai.settings import POSENET_PATH

from .network import PoseNetwork

def load_model():
    model = PoseNetwork()
    load_dict = torch.load(POSENET_PATH)
    model.load_state_dict(load_dict)

    return model