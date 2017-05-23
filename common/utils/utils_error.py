
# Copyright 2009-2010 Joshua Roesslein
# See LICENSE for details.

class SQLException(Exception):
    def __init__(self, reason):
        self.reason = reason.encode('utf-8')

    def __str__(self):
        return self.reason
