#!/usr/bin/env python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/app/")
from app import app as application
application.secret_key = 'secret_key'
