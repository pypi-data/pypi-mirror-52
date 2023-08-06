from yams.buildobjs import RelationDefinition
from cubicweb_folder.schema import Folder
from cubicweb_file.schema import File

# XXX dirty hack to be quite sure tests won't fail due to path being >
# 64 chars
Folder.get_relation('name').constraints[0].max = 256


class filed_under(RelationDefinition):
    subject = 'File'
    object = 'Folder'


class MyFile(File):
    __specializes_schema__ = True
