from cubicweb.web.views.urlrewrite import SimpleReqRewriter, rgx


class FileReqRewriter(SimpleReqRewriter):
    rules = [
         (rgx(r'/file/(\d+)/raw(/.*)?'),
          dict(rql=r'Any X WHERE X eid \1', vid='download')),
         (rgx(r'/file/(\d+)/thumb(/.*)?'),
          dict(rql=r'Any X WHERE X eid \1', vid='thumbnail'))
    ]
