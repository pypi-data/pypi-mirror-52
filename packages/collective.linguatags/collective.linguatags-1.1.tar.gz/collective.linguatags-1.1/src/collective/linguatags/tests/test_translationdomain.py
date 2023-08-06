# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.linguatags.testing import COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING  # noqa,

import six
import unittest


class TestTranslationDomain(unittest.TestCase):

    layer = COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        from zope.i18n.interfaces import ITranslationDomain
        from zope.component import queryUtility

        self.util = queryUtility(ITranslationDomain, name="linguatags")
        self.portal.REQUEST.form["submitted"] = "1"

    def test_utility_exists(self):
        """Test if collective.linguatags is cleanly uninstalled."""
        self.assertIsNotNone(self.util)

    def test_utility_fallback(self):
        msgid = u"foö"
        self.assertEqual(msgid, self.util.translate(msgid))

    def test_utility_default(self):
        msgid = u"foö"
        default = u"bär"
        self.assertEqual(default, self.util.translate(msgid, default=default))

    def test_utility_storage(self):
        msgid = u"foö"
        default = u"bär"

        from collective.linguatags.storage import get_storage

        storage = get_storage(rw=True)
        if six.PY2:
            storage[msgid.encode("utf8")] = {"de": "defoö", "it": "itfoö"}
        else:
            storage[msgid] = {"de": "defoö", "it": "itfoö"}
        self.assertEqual(
            u"defoö", self.util.translate(msgid, target_language="de", default=default)
        )

    def test_translate_with_messagid(self):
        msgid = u"foö"
        default = u"bär"

        from collective.linguatags.storage import get_storage

        storage = get_storage(rw=True)
        if six.PY2:
            storage[msgid.encode("utf8")] = {"de": "defoö", "it": "itfoö"}
        else:
            storage[msgid] = {"de": "defoö", "it": "itfoö"}

        from zope.i18nmessageid import MessageFactory

        fac = MessageFactory("linguatags")
        msg = fac(msgid, default)

        from plone import api

        self.assertEqual(u"itfoö", api.portal.translate(msg, lang="it"))


def test_translate_with_messagid_and_negotiation(self):
    msgid = u"foö"
    default = u"bär"

    from collective.linguatags.storage import get_storage

    storage = get_storage(rw=True)
    if six.PY2:
        storage[msgid.encode("utf8")] = {"de": "defoö", "it": "itfoö", "en": "brexit"}
    else:
        storage[msgid] = {"de": "defoö", "it": "itfoö", "en": "brexit"}

    from zope.i18nmessageid import MessageFactory

    fac = MessageFactory("linguatags")
    msg = fac(msgid, default)

    from plone import api

    self.assertEqual(u"brexit", api.portal.translate(msg, context=self.portal))
