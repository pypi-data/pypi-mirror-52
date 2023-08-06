"""This module glues all components together"""

import logging
import os
import sys

from melthon.middleware import MWLoader
from melthon.middleware import MWStep


def main(middleware_dir):
    # Add current directory to path.
    # This is required to be able to load the middlewares
    sys.path.append(os.getcwd())

    # Load middlewares
    mws = MWLoader(middleware_dir)

    # Initial context
    context = {}

    # Execute middlewares "before" step
    context = mws.execute_chain(MWStep.BEFORE, context)
    logging.debug('Context after middlewares "before" step: %s', repr(context))

    # TODO: Generate pages

    # Execute middlewares "after" step
    context = mws.execute_chain(MWStep.AFTER, context)
    logging.debug('Context after middlewares "after" step: %s', repr(context))
