# Copyright (c) 2009, Digital Enterprise Research Institute (DERI),
# NUI Galway
# All rights reserved.

# author: Cosmin Basca
# email: cosmin.basca@gmail.com

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer
#      in the documentation and/or other materials provided with
#      the distribution.
#    * Neither the name of DERI nor the
#      names of its contributors may be used to endorse or promote
#      products derived from this software without specific prior
#      written permission.

# THIS SOFTWARE IS PROVIDED BY DERI ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DERI BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

# -*- coding: utf-8 -*-
__author__ = 'Cosmin Basca'

from re import match, search
from os.path import exists, abspath, join, split

# -----------------------------------------------------------------------------
#
# the version
#
# -----------------------------------------------------------------------------
version         = (1,1,6)

# -----------------------------------------------------------------------------
#
# get_svn_revision function from Django:
# http://code.djangoproject.com/browser/django/trunk/django/utils/version.py
#
# -----------------------------------------------------------------------------
def get_svn_revision(path=None):
    """ Return the `svn revision number` of the current surf source folder.

    The revision number is used by the `__version__` property.

    .. note:: This function is used `as is` from the `django` project
                see http://code.djangoproject.com/browser/django/trunk/django/utils/version.py

    """

    rev = None
    if path is None:
        path = split(abspath(__file__))[0]
    entries_path = join(path, '.svn/entries')

    if exists(entries_path):
        entries = open(entries_path, 'r').read()
        # Versions >= 7 of the entries file are flat text.  The first line is
        # the version number. The next set of digits after 'dir' is the revision.
        if match('(\d+)', entries):
            rev_match = search('\d+\s+dir\s+(\d+)', entries)
            if rev_match:
                rev = rev_match.groups()[0]
        # Older XML versions of the file specify revision as an attribute of
        # the first entries node.
        else:
            from xml.dom import minidom
            dom = minidom.parse(entries_path)
            rev = dom.getElementsByTagName('entry')[0].getAttribute('revision')

    if rev:
        return u'r%s' % rev
    return u'unknown'

# -----------------------------------------------------------------------------
#
# define the full SuRF version (with svn revision...)
#
# -----------------------------------------------------------------------------
full_version    = version + (get_svn_revision(),)

def get_version(full=False):
    """ Return SuRF's `version` as a string. If `full` is `True` than `full_version` is returned instead
    (it also includes the SVN revision number).
    """
    _version = full_version if full else version
    return '.'.join(['%s'%version_part for version_part in _version])