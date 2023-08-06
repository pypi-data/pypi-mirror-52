# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from zope.i18nmessageid import MessageFactory

import six


mf = MessageFactory("linguatags")


class KeywordsViewlet(ViewletBase):
    """Return messagestrings for keywords"""

    def display_message_string(self, keyword):
        if six.PY2 and not isinstance(keyword, six.text_type):
            keyword = keyword.decode("utf8")
        return mf(keyword)
