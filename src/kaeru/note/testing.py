# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import kaeru.note


class KaeruNoteLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=kaeru.note)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'kaeru.note:default')


KAERU_NOTE_FIXTURE = KaeruNoteLayer()


KAERU_NOTE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(KAERU_NOTE_FIXTURE,),
    name='KaeruNoteLayer:IntegrationTesting',
)


KAERU_NOTE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(KAERU_NOTE_FIXTURE,),
    name='KaeruNoteLayer:FunctionalTesting',
)


KAERU_NOTE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        KAERU_NOTE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='KaeruNoteLayer:AcceptanceTesting',
)
