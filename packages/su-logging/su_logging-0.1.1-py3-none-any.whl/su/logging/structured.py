#!/usr/bin/env python3
# pylint: disable=no-member,missing-docstring
"""
Standard structured logging for Stockholm University

Usage:
    from su.logging import structured, logging
"""
import json
import logging

import logstash_formatter


class RemoveUnusedFieldsFilter(logging.Filter):
    # pylint: disable=too-few-public-methods,no-self-use
    """Unset unused log record entries"""
    def filter(self, record):
        record.args = None
        record.created = None
        record.filename = None
        record.funcName = None
        record.levelno = None
        record.lineno = None
        record.module = None
        record.msecs = None
        record.pathname = None
        record.relativeCreated = None
        record.thread = None
        return True


class CleanNoneAndUnusedFieldsEncoder(json.JSONEncoder):
    """Remove fields which are None or unused"""
    def encode(self, o):
        for key, value in list(o.items()):
            if value is None or key == '@version':
                del o[key]
        o = super().encode(o)
        return o


for handler in logging.getLogger().handlers:
    handler.setFormatter(
        logstash_formatter.LogstashFormatterV1(
            json_cls=CleanNoneAndUnusedFieldsEncoder))
    handler.addFilter(RemoveUnusedFieldsFilter())
