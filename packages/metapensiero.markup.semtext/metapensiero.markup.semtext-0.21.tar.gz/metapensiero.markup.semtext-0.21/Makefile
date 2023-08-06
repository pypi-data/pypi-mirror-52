# -*- coding: utf-8 -*-
# :Project:   metapensiero.markup.semtext -- a Simple Enough Markup
# :Created:   Wed 23 Nov 2016 09:14:23 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017 Arstecnica s.r.l.
# :Copyright: © 2018, 2019 Lele Gaifax
#

all: help

help::
	@printf "\nDevelopment\n"
	@printf "===========\n\n"

help::
	@printf "check\n\tRun the tests suite\n"

.PHONY: check
check:
	pip install -e .
	pytest

include Makefile.release
