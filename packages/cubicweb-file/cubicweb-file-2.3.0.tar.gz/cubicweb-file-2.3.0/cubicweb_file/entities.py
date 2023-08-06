"""entity classes for File entities

:organization: Logilab
:copyright: 2003-2018 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
:contact: http://www.logilab.fr/ -- mailto:contact@logilab.fr
"""

import errno
from warnings import warn
import tempfile
import os
from os.path import join, splitext, exists, isfile, isabs

from six import text_type
from PIL.Image import open as pilopen
from PIL.Image import ANTIALIAS

from logilab.mtconverter import guess_mimetype_and_encoding
from logilab.common.deprecation import deprecated

from cubicweb import Binary
from cubicweb.entities import AnyEntity, fetch_config, adapters
from cubicweb.view import EntityAdapter
from cubicweb.predicates import is_instance, has_mimetype

from cubicweb_file.hashtools import compute_hash, check_hash


class File(AnyEntity):
    """customized class for File entities"""
    __regid__ = 'File'
    fetch_attrs, cw_fetch_order = fetch_config(['data_name', 'title'])

    def set_format_and_encoding(self):
        """try to set format and encoding according to known values (filename,
        file content, format, encoding).

        This method must be called in a before_[add|update]_entity hook else it
        won't have any effect.
        """
        assert 'data' in self.cw_edited, "missing mandatory attribute data"
        if self.cw_edited.get('data'):
            old, new = self.cw_edited.oldnewvalue('data_name')
            if hasattr(self.data, 'filename') and old == new:
                self.cw_edited['data_name'] = self.data.filename
        else:
            self.cw_edited['data_format'] = None
            self.cw_edited['data_encoding'] = None
            self.cw_edited['data_name'] = None
            return
        if 'data_format' in self.cw_edited:
            format = self.cw_edited.get('data_format')
        else:
            format = None
        if 'data_encoding' in self.cw_edited:
            encoding = self.cw_edited.get('data_encoding')
        else:
            encoding = None
        if not (format and encoding):
            format, encoding = guess_mimetype_and_encoding(
                data=self.cw_edited.get('data'),
                # use get and not get_value since data has changed, we only
                # want to consider explicitly specified values, not old ones
                filename=self.cw_edited.get('data_name'),
                format=format, encoding=encoding,
                fallbackencoding=self._cw.encoding)
            if format:
                self.cw_edited['data_format'] = text_type(format)
            if encoding:
                self.cw_edited['data_encoding'] = text_type(encoding)

    def dc_title(self):
        if self.title:
            return '%s (%s)' % (self.title, self.data_name)
        return self.data_name

    def size(self):
        rql = "Any LENGTH(D) WHERE X eid %(x)s, X data D"
        return self._cw.execute(rql, {'x': self.eid})[0][0]

    def read(self, size=-1):
        return self.data.read(size)

    def seek(self, pos, *args, **kwargs):
        return self.data.seek(pos, *args, **kwargs)

    def tell(self):
        return self.data.tell()

    def icon_url(self):
        config = self._cw.vreg.config
        for rid in (self.data_format.replace('/', '_', 1),
                    self.data_format.split('/', 1)[0],
                    'default'):
            iconfile = rid + '.ico'
            rpath, iconfile = config.locate_resource(join('icons', iconfile))
            if rpath is not None:
                return self._cw.data_url(iconfile)

    def check_hash(self):
        """Return True if stored hash value is equal to the computed one from
        currently stored data.

        True if no hash is stored (typically when 'compute-hash' config option
        is false)

        """
        if self.data_hash:
            return check_hash(self.data_hash, self.data
                              and self.data.getvalue())
        return True

    def compute_hash(self, value=None, alg=None):

        """Compute the hash "value" data using "alg" hash algorithm.
        Returns a string "{ALG}HASH"

        If value is None, use stored data value.

        If alg is None, use currently configured hash algorithm (hash-algorithm
        in instance config options).

        """

        if value is None and self.data is not None:
            value = self.data.getvalue()
        if value is not None:
            if alg is None:
                alg = self._cw.vreg.config['hash-algorithm']
            return compute_hash(value, alg)

    @property
    def hash_value(self):
        """Return the hash of the currently stored data, as a string like "{ALG}HASH"

        If the hash as already been computed and stored as data_hash attribute,
        it is returned, otherwise, it is computed.

        Note that no check is performed to unsure returned hash is still valid
        for currently stored data.

        """
        if self.data_hash:
            return self.data_hash
        return self.compute_hash()

    @deprecated('[file 2.1] use entity.compute_hash() instead')
    def compute_sha1hex(self, value=None):
        return self.compute_hash(value, alg='sha1')

    @deprecated('[file 1.9] use entity.cw_adapt_to("IDownloadable")'
                '.download_url() instead')
    def download_url(self):
        return self.cw_adapt_to('IDownloadable').download_url()

    @deprecated('[file 1.9] use entity.cw_adapt_to("IDownloadable")'
                '.download_content_type() instead')
    def download_content_type(self):
        return self.cw_adapt_to('IDownloadable').download_content_type()

    @deprecated('[file 1.9] use entity.cw_adapt_to("IDownloadable")'
                '.download_encoding() instead')
    def download_encoding(self):
        return self.cw_adapt_to('IDownloadable').download_encoding()

    @deprecated('[file 1.9] use entity.cw_adapt_to("IDownloadable")'
                '.download_file_name() instead')
    def download_file_name(self):
        return self.cw_adapt_to('IDownloadable').download_file_name()

    @deprecated('[file 1.9] use entity.cw_adapt_to("IDownloadable")'
                '.download_data() instead')
    def download_data(self):
        return self.cw_adapt_to('IDownloadable').download_data()

    @property
    @deprecated('[file 1.6] use entity.data_name instead')
    def name(self):
        return self.data_name


class FileIDownloadableAdapter(adapters.IDownloadableAdapter):
    __select__ = is_instance('File')

    # IDownloadable
    def download_url(self, **kwargs):
        # include filename in download url for nicer url
        if 'small' in kwargs:
            warn('[1.15.0] `small` keyword is deprecated, you should use '
                 'FileThumbnailAdapter.download_thumbnail instead',
                 DeprecationWarning)
        name = self._cw.url_quote(self.download_file_name())
        path = '%s/raw/%s' % (self.entity.rest_path(), name)
        return self._cw.build_url(path, **kwargs)

    def download_content_type(self):
        return self.entity.data_format

    def download_encoding(self):
        return self.entity.data_encoding

    def download_file_name(self):
        return self.entity.data_name

    def download_data(self):
        if (self.download_content_type().startswith('image/')
                and 'small' in getattr(self._cw, 'form', ())):
            # Session has no .form, have to consume force param to avoid
            # infinite recursion
            self._cw.form.pop('small')
            warn('[1.15.0] `small` keyword is deprecated, you should use '
                 'FileThumbnailAdapter.download_thumbnail instead',
                 DeprecationWarning)
            return self.entity.cw_adapt_to('IThumbnail').thumbnail_data()
        return self.entity.data.getvalue()


def thumb_cache_dir(config):
    """Return the directory to use for thumbnails cache

    This function creates the directory if necessary.
    Returns None if cannot cache"""
    directory = config['thumbnail-cache-directory']
    if directory is None:
        directory = join(config.appdatahome, 'cache', 'file', 'thumbnail')
    else:
        if not isabs(directory):
            config.warning('thumbnail-cache-directory must be '
                           'an absolute existing path')
            return None
    try:
        os.makedirs(directory)
    except Exception as e:
        if not isinstance(e, OSError) or e.errno != errno.EEXIST:
            config.warning('thumbnail-cache-directory does not exists '
                           'and cannot be created, '
                           'check your filesystem permissions')
            return
    return directory


# This adapter should not be considered as an official API to manage
# thumbnails for any kind of document/content. A proper and generic
# API might be proposed in the future
class FileThumbnailAdapter(EntityAdapter):
    __regid__ = 'IThumbnail'
    __select__ = is_instance('File') & has_mimetype('image/')

    def _thumbnail_path(self):
        """Default implementation of the path generation for a thumbnail of an image
        file based on the hash of the image.

        If hash is not stored (typically when 'compute-hash' config option is
        False), the hash is computed from the image data.

        This generates a path like:

        <thumbnail-cache-directory>/<hash>_<thum_size>.png

        Note that if the stored hash value is out of sync with stored data
        value, it may produce an incorrect path (may occur if modifications are
        done with the 'hash' hooks disabled).

        """
        cachedir = thumb_cache_dir(self._cw.vreg.config)
        if cachedir:
            hashhex = self.entity.hash_value
            size = self._cw.vreg.config['image-thumb-size']
            return join(cachedir, '%s_%s.png' % (hashhex, size))
        return None

    def thumbnail_file_name(self):
        name, _ext = splitext(self.entity.data_name)
        size = self._cw.vreg.config['image-thumb-size']
        return '%s_%s.png' % (name, size)

    def thumbnail_url(self):
        name = self._cw.url_quote(self.thumbnail_file_name())
        path = '%s/thumb/%s' % (self.entity.rest_path(), name)
        return self._cw.build_url(path)

    def thumbnail_data(self):
        thumbpath = self._thumbnail_path()
        # use cache if it exists
        if thumbpath is not None:
            if isfile(thumbpath):
                try:
                    return open(thumbpath, 'rb').read()
                except IOError:
                    self.warning('Failed to load cached thumbnail file %s',
                                 thumbpath)
        iimage = self.entity.cw_adapt_to('IImage')
        try:
            data = iimage.thumbnail().getvalue()
        except UnResizeable:
            self.info('Failed to generate thumbnail for %s', self.entity.eid)
            return ''
        # fill cache if possible
        if thumbpath is not None:
            try:
                with tempfile.NamedTemporaryFile(
                        delete=False,
                        prefix=thumb_cache_dir(self._cw.vreg.config)) as tmp:
                    tmp.write(data)
                try:
                    os.rename(tmp.name, thumbpath)
                except Exception:
                    os.unlink(tmp.name)
                    raise
            except EnvironmentError:
                self.warning('Failed to save thumbnail in %s', thumbpath)
        return data

    def thumbnail_path(self):
        path = self._thumbnail_path()
        if path and exists(path):
            return path
        return None


class UnResizeable(Exception):
    pass


class IImageAdapter(EntityAdapter):
    __regid__ = 'IImage'
    __select__ = has_mimetype('image/')

    def __init__(self, *args, **kwargs):
        super(IImageAdapter, self).__init__(*args, **kwargs)
        idownloadable = self.entity.cw_adapt_to('IDownloadable')
        for meth in ('download_url', 'download_content_type',
                     'download_encoding', 'download_file_name',
                     'download_data'):
            setattr(self, meth, getattr(idownloadable, meth))

    def resize(self, size):
        size = tuple(int(s) for s in size.split('x'))
        idownloadable = self.entity.cw_adapt_to('IDownloadable')
        ctype = idownloadable.download_content_type()
        fmt = ctype and ctype.split('/', 1)[1] or None
        if fmt is None:
            self.error('unable to resize')
            raise UnResizeable
        data = idownloadable.download_data()
        pilimg = pilopen(Binary(data))
        pilimg.thumbnail(size, ANTIALIAS)
        stream = Binary()
        pilimg.save(stream, fmt)
        stream.seek(0)
        stream.filename = idownloadable.download_file_name()
        return stream

    def thumbnail(self, shadow=False, size=None):
        if size is None:
            size = self._cw.vreg.config['image-thumb-size']
        size = tuple(int(s) for s in size.split('x'))
        idownloadable = self.entity.cw_adapt_to('IDownloadable')
        data = idownloadable.download_data()
        try:
            pilimg = pilopen(Binary(data))
        except IOError:
            raise UnResizeable
        if shadow:
            self.warning('[1.15.0] the shadow parameter is now unused '
                         'and you should use css rules to lay shadows out',
                         DeprecationWarning)
        pilimg.thumbnail(size, ANTIALIAS)
        stream = Binary()
        pilimg.save(stream, 'png')
        stream.seek(0)
        ithumbnail = self.entity.cw_adapt_to('IThumbnail')
        stream.filename = ithumbnail.thumbnail_file_name()
        return stream
