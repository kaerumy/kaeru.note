# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from kaeru.note.testing import KAERU_NOTE_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that kaeru.note is properly installed."""

    layer = KAERU_NOTE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])

    def test_product_installed(self):
        """Test if kaeru.note is installed."""
        self.assertTrue(self.installer.is_product_installed('kaeru.note'))

    def test_browserlayer(self):
        """Test that IKaeruNoteLayer is registered."""
        from kaeru.note.interfaces import IKaeruNoteLayer
        from plone.browserlayer import utils
        self.assertIn(
            IKaeruNoteLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = KAERU_NOTE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal, self.layer['request'])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('kaeru.note')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if kaeru.note is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed('kaeru.note'))

    def test_browserlayer_removed(self):
        """Test that IKaeruNoteLayer is removed."""
        from kaeru.note.interfaces import IKaeruNoteLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IKaeruNoteLayer,
            utils.registered_layers())
