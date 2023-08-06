# -*- coding: utf-8 -*-
"""MX class file."""

from bits.mx.update import Update


class MX(object):
    """MX class."""

    def __init__(
        self,
        aliases_puppetdir="puppet/aliases",
        transports_puppetdir="puppet/transports",
        extension='',
        auth=None,
    ):
        """Initialize an MX class instance."""
        self.aliases_puppetdir = aliases_puppetdir
        self.transports_puppetdir = transports_puppetdir
        self.extension = extension

        self.auth = auth
        self.verbose = False
        if self.auth:
            self.verbose = self.auth.verbose

    def update(self):
        """Return an instance of the Update class."""
        return Update(self)
