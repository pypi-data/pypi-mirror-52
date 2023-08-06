# pylint: disable-msg=W0622
"""cubicweb-file packaging information"""

modname = 'cubicweb_file'
distname = "cubicweb-file"

numversion = (2, 3, 0)
version = '.'.join(str(num) for num in numversion)

license = 'LGPL'
author = "Logilab"
author_email = "contact@logilab.fr"
web = 'https://www.cubicweb.org/project/%s' % distname
description = "file component for the CubicWeb framework"
classifiers = [
           'Environment :: Web Environment',
           'Framework :: CubicWeb',
           'Programming Language :: Python',
           'Programming Language :: JavaScript',
]

__depends__ = {'cubicweb': '>= 3.24',
               'Pillow': None,
               }

__recommends__ = {}
