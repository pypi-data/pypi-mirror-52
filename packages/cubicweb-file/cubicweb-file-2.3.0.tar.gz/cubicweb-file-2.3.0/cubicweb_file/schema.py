# pylint: disable-msg=E0611,F0401

from cubicweb import _

from yams.buildobjs import EntityType, String, Bytes, RichString


class File(EntityType):
    """a downloadable file which may contains binary data"""
    title = String(fulltextindexed=True, maxsize=256)
    data = Bytes(required=True, description=_('file to upload'))
    data_format = String(
        required=True, maxsize=128,
        description=_('MIME type of the file. Should be dynamically set '
                      'at upload time.'))
    data_encoding = String(
        maxsize=32,
        description=_('encoding of the file when it applies (e.g. text). '
                      'Should be dynamically set at upload time.'))
    data_name = String(
        required=True, fulltextindexed=True,
        description=_('name of the file. Should be dynamically set '
                      'at upload time.'))
    data_hash = String(
        maxsize=256,  # max len of currently available hash alg + prefix is 140
        description=_('hash of the file. May be set at upload time.'),
        __permissions__={'read': ('managers', 'users', 'guests'),
                         'add': (),
                         'update': ()})
    description = RichString(fulltextindexed=True, internationalizable=True,
                             default_format='text/rest')
