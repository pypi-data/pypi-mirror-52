.. -*- coding: utf-8 -*-
.. (c) 2019 Andreas Motl <andreas.motl@ip-tools.org>

####################
OPS API access tests
####################

See also `OPS version 3.2 documentation – version 1.3.8`_.

.. _OPS version 3.2 documentation – version 1.3.8: http://documents.epo.org/projects/babylon/eponet.nsf/0/F3ECDCC915C9BCD8C1258060003AA712/$File/ops_v3.2_documentation_-_version_1.3.81_en.pdf

>>> from patzilla.util.web.pyramid.commandline import setup_commandline_pyramid
>>> from patzilla.access.epo.ops.commands import fulltext_languages

>>> setup_commandline_pyramid(configfile)


Fulltext inquiry
================
>>> fulltext_languages('EP.0666666.B1')
