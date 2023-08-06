
from cubicweb import Binary
from cubicweb.devtools import testlib, ApptestConfiguration
from cubicweb_file.ccplugin import FileRefreshHashCommand
from cubicweb.server.serverconfig import ServerConfiguration


class FileRefreshCommandTC(testlib.CubicWebTC):

    def setUp(self):
        super(FileRefreshCommandTC, self).setUp()
        self.orig_config_for = ServerConfiguration.config_for

        def config_for(appid):
            return ApptestConfiguration(appid, __file__)

        ServerConfiguration.config_for = staticmethod(config_for)

    def tearDown(self):
        ServerConfiguration.config_for = self.orig_config_for
        super(FileRefreshCommandTC, self).tearDown()

    def test_refresh(self):
        with self.admin_access.repo_cnx() as cnx:
            cnx.vreg.config['compute-hash'] = 0
            for i in range(10):
                fobj = cnx.create_entity(
                    'File', data_name=u"foo%d.txt" % i,
                    data_format=u'text/plain',
                    data=Binary(b"xxx"))
                self.assertEqual(None, fobj.data_hash)
            for i in range(10):
                fobj = cnx.create_entity(
                    'MyFile', data_name=u"foo%s.png" % i,
                    data_format=u'image/png',
                    data=Binary(b"xxx"))
                self.assertEqual(None, fobj.data_hash)
            cnx.commit()
        FileRefreshHashCommand(None).run([self.appid])
        with self.admin_access.repo_cnx() as cnx:
            self.assertFalse(cnx.execute('Any X WHERE X is_instance_of File, '
                                         'NOT X data_hash NULL'))

        cmd = FileRefreshHashCommand(None)
        cmd.config.force = True
        cmd.run([self.appid])
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(
                10,
                len(cnx.execute('Any X WHERE X is_instance_of File, '
                                'X data_hash LIKE "{sha256}%"')))

        cmd.config.subclasses = True
        cmd.run([self.appid])
        with self.admin_access.repo_cnx() as cnx:
            self.assertEqual(
                20,
                len(cnx.execute('Any X WHERE X is_instance_of File, '
                                'X data_hash LIKE "{sha256}%"')))


if __name__ == '__main__':
    from unittest import main
    main()
