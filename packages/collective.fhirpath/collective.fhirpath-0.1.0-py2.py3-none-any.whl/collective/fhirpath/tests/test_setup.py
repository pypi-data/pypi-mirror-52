# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.fhirpath.testing import \
    COLLECTIVE_FHIRPATH_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.fhirpath is properly installed."""

    layer = COLLECTIVE_FHIRPATH_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.fhirpath is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.fhirpath'))

    def test_browserlayer(self):
        """Test that ICollectiveFhirpathLayer is registered."""
        from collective.fhirpath.interfaces import (
            ICollectiveFhirpathLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveFhirpathLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_FHIRPATH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.fhirpath'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.fhirpath is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.fhirpath'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveFhirpathLayer is removed."""
        from collective.fhirpath.interfaces import \
            ICollectiveFhirpathLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveFhirpathLayer,
            utils.registered_layers())
