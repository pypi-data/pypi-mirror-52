# -*- coding: utf-8 -*-
# (c) 2014-2019 Andreas Motl <andreas.motl@ip-tools.org>
import logging
from patzilla.util.web.pyramid.commandline import setup_commandline_pyramid

def boot():
    configfile =
    env = setup_commandline_pyramid(configfile)
    logger = logging.getLogger(__name__)
