============
pristine-lfs
============

About
-----

**pristine-lfs** is a tool to replace *pristine-tar* by the means of using
Git LFS to store tarballs. The original *pristine-tar* tool is a way to store
binary tarballs in Git by regenerating them using only a small binary delta
file and a checkout of the upstream branch.

Installation
------------

*pristine-lfs* assumes you have Python 3.6 or later installed as ``/usr/bin/python3``.

*pristine-lfs* ships with a setup.py installer based on setuptools.
To install *pristine-lfs*, simply type::

    ./setup.py install

This will install *pristine-lfs* itself, its manpage and this README file into
their proper locations.

Alternatively, to install via ``pip``, run::

    pip install pristine-lfs


License
-------

This program is free software; you can redistribute it
and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE.  See the GNU General Public License version 2
text for more details.

You should have received a copy of the GNU General Public
License along with this package; if not, write to the Free
Software Foundation, Inc., 51 Franklin St, Fifth Floor,
Boston, MA  02110-1301 USA

Authors
-------

For the list of contributors, see CONTRIBUTORS.
