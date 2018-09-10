#!/usr/bin/env python
# -*- coding: utf8 -*-

from wsgiref.handlers import CGIHandler
from app import app

CGIHandler().run(app)
