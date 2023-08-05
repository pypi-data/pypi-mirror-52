import zope.i18nmessageid
import pkg_resources

_ = zope.i18nmessageid.MessageFactory('ftw.footer')

IS_PLONE_5 = pkg_resources.get_distribution('Products.CMFPlone').version >= '5'
