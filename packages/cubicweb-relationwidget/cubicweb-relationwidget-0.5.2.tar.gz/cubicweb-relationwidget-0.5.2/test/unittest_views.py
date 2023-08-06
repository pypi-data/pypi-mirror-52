# copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""Unittests of relationwidget cube views"""

from cubicweb.__pkginfo__ import numversion as cwversion
from cubicweb.devtools.testlib import CubicWebTC


class ViewTC(CubicWebTC):
    """
    Mind test/data/views.py for the uicfg.
    """

    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            for num in range(10):
                cnx.create_entity('CWGroup', name=u'group_%d' % num)
            cnx.commit()

    def triggers_for(self, pageinfo, rtype):
        xpath = '//div[@id="%s-subject_row"]//a' % rtype
        return sorted(a.text for a in pageinfo.etree.xpath(xpath)
                      if 'relationwidget' in a.get('onclick', ''))

    def values_for(self, pageinfo, eid, rtype):
        xpath = '//div[@id="inputs-for-widget-%s-subject-%s"]//a' % (rtype, eid)
        return [a.get('href', '') for a in pageinfo.etree.xpath(xpath)]

    def modal(self, req, relation='in_group:CWGroup:subject', **form):
        req.form.update(form)
        req.form['relation'] = relation
        return self.view('search_related_entities', req.user.as_rset(),
                         req=req, template=None)

    def test_triggers(self):
        """
        Check we get the right number of modal dialog trigger depending on the
        relation's target entity types.
        """
        with self.admin_access.web_request() as req:
            pageinfo = self.view('edition', req.user.as_rset(), req)
            self.assertEqual(['link to CWGroup'],
                             self.triggers_for(pageinfo, 'in_group'))
            self.assertEqual(['CWGroup', 'MyThing'],
                             self.triggers_for(pageinfo, 'my_relation'))

    def test_init_value_from_existing(self):
        with self.admin_access.web_request() as req:
            user = req.user
            req.create_entity('CWGroup', name=u'g', reverse_in_group=user,
                              reverse_my_relation=user)
            req.create_entity('MyThing', label=u't1', reverse_my_relation=user)
            req.create_entity('MyThing', label=u't2', reverse_my_relation=user)
            pageinfo = self.view('edition', user.as_rset(), req)
            self.assertCountEqual(
                [g.absolute_url() for g in user.in_group],
                self.values_for(pageinfo, user.eid, 'in_group'))
            self.assertCountEqual(
                [o.absolute_url() for o in user.my_relation],
                self.values_for(pageinfo, user.eid, 'my_relation'))

    def test_init_value_from_uicfg(self):
        with self.admin_access.web_request() as req:
            # see test/data/views.py for corresponding uicfg
            group = req.create_entity('CWGroup', name=u'init_group')
            pageinfo = self.view('creation', None, etype='CWUser',
                                 template=None, req=req)
            self.assertCountEqual([group.absolute_url()],
                                  self.values_for(pageinfo, 'A', 'in_group'))

    def test_navigation_size(self):
        if cwversion < (3, 23):
            self.skipTest('this test is relevant only if cubicweb version >= 3.23')
        xpath = '//div[@id="cw-relationwidget-table-%s"]//tbody//tr'

        def row_nb(pageinfo, eid): return len(pageinfo.etree.xpath(xpath % eid))
        with self.admin_access.web_request() as req:
            self.assertEqual(10, row_nb(self.modal(req), req.user.eid))
        with self.admin_access.client_cnx() as cnx:
            cnx.user.set_property(u'relationwidget.table-page-size', 3)
            cnx.commit()
        with self.admin_access.web_request() as req:
            self.assertEqual(
                req.user.properties['relationwidget.table-page-size'], '3')
            self.assertEqual(3, row_nb(self.modal(req), req.user.eid))

    def test_navigation_display_all(self):
        if cwversion < (3, 23):
            self.skipTest('this test is relevant only if cubicweb version >= 3.23')

        def has_total(pageinfo): return any(
            'rw-total-size' in tag.get('class')
            for tag in pageinfo.etree.xpath('//ul'))
        with self.admin_access.web_request() as req:
            self.assertFalse(has_total(self.modal(req)))
        with self.admin_access.client_cnx() as cnx:
            cnx.user.set_property(u'relationwidget.display-all-limit', 5)
            cnx.commit()
        with self.admin_access.web_request() as req:
            self.assertEqual(
                req.user.properties['relationwidget.display-all-limit'], '5')
            self.assertTrue(has_total(self.modal(req)))

    def test_creation_form(self):
        tabs_xpath = '//ul[@role="tablist"]//li'

        def tab_nb(pageinfo): return len(pageinfo.etree.xpath(tabs_xpath))
        with self.admin_access.web_request() as req:
            self.assertEqual(2, tab_nb(self.modal(req)))
            self.assertEqual(1, tab_nb(self.modal(req, no_creation_form='1')))

    def test_no_duplicate_with_linkto(self):
        with self.admin_access.web_request() as req:
            group = req.create_entity('CWGroup', name=u'init_group',
                                      reverse_in_group=req.user)
            req.form['__linkto'] = 'in_group:%s:subject' % group.eid
            pageinfo = self.view('edition', req.user.as_rset(), req)
            self.assertCountEqual(
                [g.absolute_url() for g in req.user.in_group],
                self.values_for(pageinfo, req.user.eid, 'in_group'))


if __name__ == "__main__":
    from logilab.common.testlib import unittest_main
    unittest_main()
