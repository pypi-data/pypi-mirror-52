#!/usr/bin/env python3
# pylint: disable=import-error,missing-docstring,no-member,no-name-in-module
"""
Add logging to stdout

Usage:
    from su.logging import console, logging
"""

import logging
import sys

HANDLER = logging.StreamHandler(sys.stdout)
LOGGER = logging.getLogger()
LOGGER.addHandler(HANDLER)
