from AccessControl import getSecurityManager
from Acquisition._Acquisition import aq_parent
from ftw.footer import IS_PLONE_5
from ftw.footer.interfaces import IFooterSettings
from plone.app.layout.viewlets import common
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.registry.interfaces import IRegistry
from Products.CMFCore.interfaces import IContentish
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.component import getUtility


GRIDCOLS = 12 if IS_PLONE_5 else 16  # poss make configurable thru registry


class FooterViewlet(common.ViewletBase):
    index = ViewPageTemplateFile('footer_viewlet.pt')

    def __init__(self, context, request, view, manager=None):
        super(FooterViewlet, self).__init__(context, request, view, manager)

        # Set context to closest content to adapt the assignment mapping.
        self.context = context
        while not IContentish.providedBy(self.context) and \
                not IPloneSiteRoot.providedBy(self.context):
            self.context = aq_parent(self.context)

    def calculate_width(self):
        columns = self.get_column_count()
        width = GRIDCOLS / columns
        return width

    # Redundant in Plone 5
    def calculate_index(self, manager):
        self.managers = self.get_managers()
        index = self.managers[manager]['index']
        return (index - 1) * self.calculate_width()

    def get_managers(self):
        managers = {}
        for counter in range(1, 5):
            pm_name = 'ftw.footer.column{}'.format(counter)
            manager = getUtility(IPortletManager, name=pm_name)
            mapping = getMultiAdapter((self.context, manager),
                                      IPortletAssignmentMapping).__of__(self.context)
            managers[pm_name] = {
                'empty': not bool(mapping.keys()), 'index': counter}
        return managers

    def generate_classes(self, manager):
        width = self.calculate_width()
        if IS_PLONE_5:
            classes = 'col-lg-{}'.format(width)
        else:
            index = self.calculate_index(manager)
            classes = 'column cell position-{} width-{}'.format(index, width)
        return classes

    def is_column_visible(self, index):
        columns = self.get_column_count()
        return bool(index <= columns)

    def can_manage(self):
        if IS_PLONE_5:
            return False
        sm = getSecurityManager()
        return bool(sm.checkPermission('ftw.footer: Manage Footer',
                                       self.context))

    def get_column_count(self):
        registry = getUtility(IRegistry)
        footer_settings = registry.forInterface(IFooterSettings,
                                                check=False)
        if not footer_settings:
            return 0
        count = footer_settings.columns_count
        return count
