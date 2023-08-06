# -*- coding: utf-8 -*-

from os.path import join, dirname
from PIL.Image import open as pilopen

from cubicweb import Binary, Unauthorized
from cubicweb.devtools.testlib import CubicWebTC


class FileTC(CubicWebTC):

    def test_set_mime_and_encoding(self):
        with self.admin_access.client_cnx() as cnx:
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt", data=Binary(b"xxx"))
            self.assertEqual(fobj.data_format, u'text/plain')
            self.assertEqual(fobj.data_encoding, cnx.encoding)

    def test_set_mime_and_encoding_gz_file(self):
        with self.admin_access.client_cnx() as cnx:
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt.gz", data=Binary(b"xxx"))
            self.assertEqual(fobj.data_format, u'text/plain')
            self.assertEqual(fobj.data_encoding, u'gzip')
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt.gz", data=Binary(b"xxx"),
                data_format='application/gzip')
            self.assertEqual(fobj.data_format, u'text/plain')
            self.assertEqual(fobj.data_encoding, u'gzip')
            fobj = cnx.create_entity(
                'File', data_name=u"foo.gz", data=Binary(b"xxx"))
            self.assertEqual(fobj.data_format, u'application/gzip')
            self.assertEqual(fobj.data_encoding, None)

    def test_set_mime_and_encoding_bz2_file(self):
        with self.admin_access.client_cnx() as cnx:
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt.bz2", data=Binary(b"xxx"))
            self.assertEqual(fobj.data_format, u'text/plain')
            self.assertEqual(fobj.data_encoding, u'bzip2')
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt.bz2", data=Binary(b"xxx"),
                data_format='application/bzip2')
            self.assertEqual(fobj.data_format, u'text/plain')
            self.assertEqual(fobj.data_encoding, u'bzip2')
            fobj = cnx.create_entity(
                'File', data_name=u"foo.bz2", data=Binary(b"xxx"))
            self.assertEqual(fobj.data_format, u'application/bzip2')
            self.assertEqual(fobj.data_encoding, None)

    def test_set_mime_and_encoding_unknwon_ext(self):
        with self.admin_access.client_cnx() as cnx:
            fobj = cnx.create_entity(
                'File', data_name=u"foo.123", data=Binary(b"xxx"))
            self.assertEqual(fobj.data_format, u'application/octet-stream')
            self.assertEqual(fobj.data_encoding, None)


class ImageTC(CubicWebTC):

    @property
    def data(self):
        with open(join(dirname(__file__), 'data', '20x20.gif'), 'rb') as fobj:
            return fobj.read()

    def test_resize_image(self):
        with self.admin_access.client_cnx() as cnx:
            # check no resize
            img = cnx.create_entity(
                'File', data=Binary(self.data), data_name=u'20x20.gif')
            self.assertEqual(img.data_format, u'image/gif')
            self.assertEqual(img.data.getvalue(), self.data)
            # check thumb
            self.set_option('image-thumb-size', '5x5')
            pilthumb = pilopen(
                img.cw_adapt_to('IImage').thumbnail(shadow=False))
            self.assertEqual(pilthumb.size, (5, 5))
            self.assertEqual('PNG', pilthumb.format)
            # check resize 10x5
            self.set_option('image-max-size', '10x5')
            img = cnx.create_entity(
                'File', data=Binary(self.data), data_name=u'20x20.gif')
            self.assertEqual(img.data_format, u'image/gif')
            pilimg = pilopen(img.data)
            self.assertEqual(pilimg.size, (5, 5))
            # also on update
            img.cw_set(data=Binary(self.data))
            img.cw_clear_all_caches()
            pilimg = pilopen(img.data)
            self.assertEqual(pilimg.size, (5, 5))
            # test image smaller than max size
            self.set_option('image-max-size', '40x40')
            img.cw_set(data=Binary(self.data))
            pilimg = pilopen(img.data)
            self.assertEqual(pilimg.size, (20, 20))


class HashTC(CubicWebTC):

    def test_init_hash(self):
        with self.admin_access.client_cnx() as cnx:
            cnx.vreg.config['compute-hash'] = 0
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt", data=Binary(b"xxx"))
            self.assertEqual(None, fobj.data_hash)

            cnx.vreg.config['compute-hash'] = 1
            cnx.vreg.config['hash-algorithm'] = 'sha256'
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt", data=Binary(b"xxx"))
            self.assertEqual(
                '{sha256}cd2eb0837c9b4c962c22d2ff8b5441b7b45805887f051d39bf133b583baf6860',  # noqa
                fobj.data_hash)

    def test_modify_data(self):
        with self.admin_access.client_cnx() as cnx:
            cnx.vreg.config['compute-hash'] = 1
            cnx.vreg.config['hash-algorithm'] = 'sha256'
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt", data=Binary(b"xxx"))
            fobj.cw_set(data=Binary(b'yyy'))
            self.assertEqual(
                '{sha256}f2afd1cacb5441a5e65a7a460a5f9898b7b98b08aa6323a2e53c8b9a9686cd86',  # noqa
                fobj.data_hash)

    def test_manual_set_hash_forbidden(self):
        with self.admin_access.client_cnx() as cnx:
            cnx.vreg.config['compute-hash'] = 0
            with self.assertRaises(Unauthorized):
                cnx.create_entity(
                    'File', data_name=u"foo.txt", data=Binary(b"xxx"),
                    data_hash=u'0'*40)
                cnx.commit()

    def test_hash_algos(self):
        with self.admin_access.client_cnx() as cnx:
            cnx.vreg.config['compute-hash'] = 1
            cnx.vreg.config['hash-algorithm'] = 'sha256'
            fobj = cnx.create_entity(
                'File', data_name=u"foo.txt", data=Binary(b"xxx")).eid
            cnx.commit()
        with self.admin_access.client_cnx() as cnx:
            fobj = cnx.find('File', eid=fobj).one()

            cnx.vreg.config['hash-algorithm'] = 'md5'
            fobj.cw_set(data=Binary(b'md5'))
            fobj.cw_clear_all_caches()
            self.assertEqual(
                '{md5}1bc29b36f623ba82aaf6724fd3b16718',
                fobj.data_hash)

            cnx.vreg.config['hash-algorithm'] = 'sha1'
            fobj.cw_set(data=Binary(b'sha1'))
            fobj.cw_clear_all_caches()
            self.assertEqual(
                '{sha1}415ab40ae9b7cc4e66d6769cb2c08106e8293b48',
                fobj.data_hash)

            cnx.vreg.config['hash-algorithm'] = 'sha512'
            fobj.cw_set(data=Binary(b'sha512'))
            fobj.cw_clear_all_caches()
            self.assertEqual(
                '{sha512}1f9720f871674c18e5fecff61d92c1355cd4bfac25699fb7ddfe7717c9669b4d085193982402156122dfaa706885fd64741704649795c65b2a5bdec40347e28a',  # noqa
                fobj.data_hash)


if __name__ == '__main__':
    from unittest import main
    main()
