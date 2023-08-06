#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sanic_jinja2 import Environment, PackageLoader, TemplateNotFound
from sanic_jinja2 import _make_new_gettext, _make_new_ngettext
from sanic_jinja2_spf.plugin import sanic_jinja2, SanicJinja2

__version__ = '0.7.5'

__all__  = ['sanic_jinja2', 'Environment', 'PackageLoader', 'TemplateNotFound']

