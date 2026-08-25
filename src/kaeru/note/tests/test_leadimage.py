# -*- coding: utf-8 -*-
from kaeru.note.testing import (
    KAERU_NOTE_FUNCTIONAL_TESTING,
    KAERU_NOTE_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from plone.namedfile import NamedBlobImage
from zope.component import queryUtility

import base64
import unittest


PNG_1X1 = base64.b64decode(
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ'
    b'AAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=='
)


def make_image():
    return NamedBlobImage(
        PNG_1X1,
        contentType='image/png',
        filename='test.png',
    )


class NoteLeadImageIntegrationTest(unittest.TestCase):

    layer = KAERU_NOTE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_note_type_has_leadimage_behavior(self):
        fti = queryUtility(IDexterityFTI, name='Note')
        self.assertIn('plone.leadimage', fti.behaviors)


class NoteLeadImageFunctionalTest(unittest.TestCase):

    layer = KAERU_NOTE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.folder = api.content.create(
            container=self.portal,
            type='Folder',
            id='folder',
        )
        self.note = api.content.create(
            container=self.folder,
            type='Note',
            id='note',
            title='A note',
        )
        self.note.image = make_image()
        self.note.image_caption = 'Lead image caption'

    def test_lead_image_shown_in_all_content_view(self):
        view = self.folder.restrictedTraverse('full_view')
        result = view()
        self.assertIn('section-leadimage', result)
        self.assertIn('@@images/image', result)
        self.assertIn('Lead image caption', result)

    def test_lead_image_not_duplicated_on_note_own_view(self):
        view = self.note.restrictedTraverse('note-view')
        result = view()
        self.assertEqual(result.count('section-leadimage'), 1)

    def test_no_lead_image_section_without_image(self):
        folder = api.content.create(
            container=self.portal,
            type='Folder',
            id='folder2',
        )
        api.content.create(
            container=folder,
            type='Note',
            id='note2',
            title='A note without image',
        )
        view = folder.restrictedTraverse('full_view')
        result = view()
        self.assertNotIn('section-leadimage', result)
