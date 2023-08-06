#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Rich Lewis <opensource@richlew.is>
"""
richprompt
~~~~~~~~~~

A better prompt for the IPython interactive shell.
"""

from .prompts import RichPrompts
from .magic import load_ipython_extension
from .magic import unload_ipython_extension
from .startup import load
from .startup import unload
from .timer import Timer

__author__ = "Rich Lewis"
__copyright__ = "Copyright 2019, Rich Lewis"
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Rich Lewis"
__email__ = "opensource@richlew.is"
