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


class CleanNoneAndUnusedFieldsEncoder(json.JSONEncoder):
    """Remove fields which are None or unused"""
    def encode(self, o):
        unused_fields = (
            '@version',
            'args',
            'created',
            'filename',
            'funcName',
            'levelno',
            'lineno',
            'module',
            'msecs',
            'pathname',
            'relativeCreated',
            'thread',
        )
        for key, value in list(o.items()):
            if value is None or key in unused_fields:
                del o[key]

        o = super().encode(o)
        return o


for handler in logging.getLogger().handlers:
    handler.setFormatter(
        logstash_formatter.LogstashFormatterV1(
            json_cls=CleanNoneAndUnusedFieldsEncoder))
