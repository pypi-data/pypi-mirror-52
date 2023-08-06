#!/usr/bin/env python3
# pylint: disable=import-self,no-name-in-module,no-member,import-error
"""
Standard logging for Stockholm University

Usage:
    from su.logging import logging
"""

import logging
import logging.handlers

HANDLER = logging.handlers.SysLogHandler()
logging.basicConfig(handlers=[HANDLER])
