import hashlib

options = (
    ('image-max-size',
     {'type': 'string',
      'default': None,
      'help': 'all images will be resized to this max size if set',
      'group': 'file',
      'level': 2,
      }),
    ('image-thumb-size',
     {'type': 'string',
      'default': '75x75',
      'help': 'thumbnail size of your images',
      'group': 'file',
      'level': 2,
      }),
    ('thumbnail-cache-directory',
     {'type': 'string',
      'default': None,
      'help': ('Cache directory for thumbnails (if unset, defaults '
               'to INSTANCEDIR/cache/file/thumbnails) '
               'if set, must be an absolute path).'),
      'level': 2,
      'group': 'file'
      }),
    ('compute-hash',
     {'type': 'yn',
      'default': False,
      'help': 'compute hash digest of your files',
      'group': 'file',
      'level': 2,
      }),
    ('hash-algorithm',
     {'type': 'choice',
      'default': 'sha256',
      'choices': list(hashlib.algorithms_available),
      'help': ('hash algorithm used to compute hash of your files (%s)' %
               ', '.join(sorted(hashlib.algorithms_available))),
      'group': 'file',
      'level': 2,
      }),
    )
