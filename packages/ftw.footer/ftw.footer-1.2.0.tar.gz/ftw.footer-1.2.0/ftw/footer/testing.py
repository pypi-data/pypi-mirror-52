from ftw.builder.content import register_dx_content_builders
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig


class FtwFooterLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        # The tests will fail with a
        # `ValueError: Index of type DateRecurringIndex not found` unless
        # the product 'Products.DateRecurringIndex' is installed.
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.footer:default')
        applyProfile(portal, 'plone.app.contenttypes:default')

        # Tell ftw.builder to use DX content types, even for Plone 4.3.
        # This is needed because Plone 5.1 needs `plone.app.contenttypes`.
        register_dx_content_builders(force=True)


FTW_FOOTER_FIXTURE = FtwFooterLayer()
FTW_FOOTER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_FOOTER_FIXTURE, ), name="FtwFooter:Integration")

FTW_FOOTER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FTW_FOOTER_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="FtwFooter:Functional")
