import importlib
import os

os.environ['PATH'] = ';'.join([os.path.abspath(os.path.dirname(__file__)), os.environ['PATH']])
from .cv2 import *
from .data import *

# wildcard import above does not import "private" variables like __version__
# this makes them available
globals().update(importlib.import_module('cv2.cv2').__dict__)
