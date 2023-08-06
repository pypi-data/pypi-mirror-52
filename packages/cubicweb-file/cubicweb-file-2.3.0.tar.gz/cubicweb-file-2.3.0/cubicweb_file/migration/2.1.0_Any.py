
subclasses = False
is_rel = 'is'

if confirm('Also handle entity types that inherit from File?'):
    subclasses = True
    is_rel = 'is_instance_of'

add_attribute('File', 'data_hash')
if subclasses:
    for etype in schema['File'].specialized_by(recursive=True):
        add_attribute(etype.type, 'data_hash')

rql('SET X data_hash "{sha1}"+H WHERE X %(rel)s File, '
    'X data_sha1hex H, '
    'NOT X data_sha1hex NULL' % {'rel': is_rel})

drop_attribute('File', 'data_sha1hex')
if subclasses:
    for etype in schema['File'].specialized_by(recursive=True):
        drop_attribute(etype.type, 'data_sha1hex')

commit()
