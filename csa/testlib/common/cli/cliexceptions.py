#!/usr/bin/env python

""" Customized CLI exceptions."""

from __future__ import absolute_import


class CliError(Exception): pass


class ConfigError(Exception): pass


class CliValueError(CliError): pass
