# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.linguatags


class CollectiveLinguatagsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.linguatags)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.linguatags:default")


COLLECTIVE_LINGUATAGS_FIXTURE = CollectiveLinguatagsLayer()


COLLECTIVE_LINGUATAGS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_LINGUATAGS_FIXTURE,),
    name="CollectiveLinguatagsLayer:IntegrationTesting",
)


COLLECTIVE_LINGUATAGS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_LINGUATAGS_FIXTURE,),
    name="CollectiveLinguatagsLayer:FunctionalTesting",
)


COLLECTIVE_LINGUATAGS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_LINGUATAGS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveLinguatagsLayer:AcceptanceTesting",
)
