# -*- coding: utf-8 -*-
"""Conda environment creation and update from meta.yaml."""
from pkg_resources import get_distribution
from pkg_resources import DistributionNotFound

try:
    __version__ = get_distribution('cenv_tool').version
except (AttributeError, DistributionNotFound):
    __version__ = ''
