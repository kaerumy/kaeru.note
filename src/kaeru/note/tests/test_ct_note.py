# -*- coding: utf-8 -*-
from kaeru.note.content.note import INote  # NOQA E501
from kaeru.note.testing import KAERU_NOTE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class NoteIntegrationTest(unittest.TestCase):

    layer = KAERU_NOTE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_note_schema(self):
        fti = queryUtility(IDexterityFTI, name='Note')
        schema = fti.lookupSchema()
        self.assertEqual(INote, schema)

    def test_ct_note_fti(self):
        fti = queryUtility(IDexterityFTI, name='Note')
        self.assertTrue(fti)

    def test_ct_note_factory(self):
        fti = queryUtility(IDexterityFTI, name='Note')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            INote.providedBy(obj),
            u'INote not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_note_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Note',
            id='note',
        )

        self.assertTrue(
            INote.providedBy(obj),
            u'INote not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('note', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('note', parent.objectIds())

    def test_ct_note_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Note')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_note_filter_content_type_false(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Note')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'note_id',
            title='Note container',
         )
        self.parent = self.portal[parent_id]
        obj = api.content.create(
            container=self.parent,
            type='Document',
            title='My Content',
        )
        self.assertTrue(
            obj,
            u'Cannot add {0} to {1} container!'.format(obj.id, fti.id)
        )
