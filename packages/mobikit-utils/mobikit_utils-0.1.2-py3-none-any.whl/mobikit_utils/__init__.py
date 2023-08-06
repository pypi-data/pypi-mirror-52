__version__ = "0.1.2"

# this is meant to fail for public installs
# we don't want to publically expose spatial package yet
try:
    from .spatial import spatial
except ImportError:
    pass

from . import utils
