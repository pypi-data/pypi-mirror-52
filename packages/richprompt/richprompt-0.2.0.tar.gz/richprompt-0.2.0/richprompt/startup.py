#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Rich Lewis <opensource@richlew.is>
"""
richprompt.load
~~~~~~~~~~~~~~~

A means of loading richprompt without magic.
"""

from IPython import get_ipython
from . import magic


def load():
    """Load the prompt for the currently active IPython shell."""
    magic.load_ipython_extension(get_ipython())


def unload():
    """Unload the prompt for the currently active IPython shell."""
    magic.unload_ipython_extension(get_ipython())
