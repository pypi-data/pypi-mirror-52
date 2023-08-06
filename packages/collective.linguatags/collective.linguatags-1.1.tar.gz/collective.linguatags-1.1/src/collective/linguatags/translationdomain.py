# -*- coding: utf-8 -*-
from collective.linguatags.storage import get_storage
from plone import api
from zope.component import getUtility
from zope.i18n.interfaces import INegotiator
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implementer

import six


@implementer(ITranslationDomain)
class TagsTranslationDomain(object):

    domain = "linguatags"

    def translate(
        self,
        msgid,
        mapping=None,
        context=None,
        target_language=None,
        default=None,
        msgid_plural=None,
        default_plural=None,
        number=None,
    ):

        msgkey = msgid
        if six.PY2 and isinstance(msgkey, six.text_type):
            msgkey = msgkey.encode("utf8")
        storage = get_storage()
        translations = storage.get(msgkey, None)

        if translations is None:
            # handle default
            if default is None:
                default = msgid
            if six.PY2 and not isinstance(default, six.text_type):
                default = default.decode("utf8")
            return default

        # find out what the target language should be
        if target_language is None and context is not None:
            langs = api.portal.get_registry_record("plone.available_languages")
            negotiator = getUtility(INegotiator)
            target_language = negotiator.getLanguage(langs, context)

        # fetch matching translation or default
        message = translations.get(target_language, default)
        if six.PY2 and not isinstance(message, six.text_type):
            return message.decode("utf-8")
        return message
