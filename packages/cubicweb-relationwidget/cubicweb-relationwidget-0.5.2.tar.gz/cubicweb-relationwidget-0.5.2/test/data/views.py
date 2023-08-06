from cubicweb.web.views import uicfg

from cubicweb_relationwidget.views import RelationFacetWidget

_afs = uicfg.autoform_section
_affk = uicfg.autoform_field_kwargs
_affk.tag_subject_of(('CWUser', 'in_group', 'CWGroup'),
                     {'widget': RelationFacetWidget})

_afs.tag_subject_of(('CWUser', 'my_relation', '*'), 'main', 'attributes')
_affk.tag_subject_of(('CWUser', 'my_relation', '*'),
                     {'widget': RelationFacetWidget})


def in_group_init_value(form, field):
    return [g.eid
            for g in form._cw.find('CWGroup', name=u'init_group').entities()]


_affk.tag_subject_of(('CWUser', 'in_group', 'CWGroup'),
                     {'value': in_group_init_value})
