import os
import logging
from dotenv import load_dotenv
load_dotenv(verbose=True)

logger = logging.getLogger(__name__)

# The Root Directory of the project
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POSENET_PATH = os.path.join(ROOT_DIR, 'data','raw','posenet.pth')
POSTURENET_PATH = os.path.join(ROOT_DIR, 'data','raw','posturenet.pth')

import torch
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
