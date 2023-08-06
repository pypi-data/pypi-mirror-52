#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Rich Lewis <opensource@richlew.is>
"""
richprompt.magic
~~~~~~~~~~~~~~~~

A means of adding richprompt with ipython magic.
"""

from .prompts import RichPrompts
from IPython import get_ipython

OLD_PROMPTS = None

def load_ipython_extension(ipython):
    global OLD_PROMPTS
    OLD_PROMPTS, ipython.prompts = ipython.prompts, RichPrompts(ipython)


def unload_ipython_extension(ipython):
    global OLD_PROMPTS
    OLD_PROMPTS, ipython.prompts = RichPrompts(ipython), ipython.prompts
