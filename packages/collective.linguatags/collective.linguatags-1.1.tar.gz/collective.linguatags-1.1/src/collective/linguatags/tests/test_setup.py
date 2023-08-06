# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.linguatags.testing import COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING  # noqa,
from plone import api

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.linguatags is properly installed."""

    layer = COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.linguatags is installed."""
        self.assertTrue(self.installer.isProductInstalled("collective.linguatags"))

    def test_browserlayer(self):
        """Test that ICollectiveLinguatagsLayer is registered."""
        from collective.linguatags.interfaces import ICollectiveLinguatagsLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveLinguatagsLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        self.installer.uninstallProducts(["collective.linguatags"])

    def test_product_uninstalled(self):
        """Test if collective.linguatags is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("collective.linguatags"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveLinguatagsLayer is removed."""
        from collective.linguatags.interfaces import ICollectiveLinguatagsLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveLinguatagsLayer, utils.registered_layers())
