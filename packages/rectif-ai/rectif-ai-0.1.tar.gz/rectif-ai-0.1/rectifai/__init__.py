import sys

if sys.version_info < (3, 6, 1):
    raise RuntimeError("Rectif.ai requires Python 3.6 or later")

from rectifai.version import VERSION as __version__