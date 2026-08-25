# -*- coding: utf-8 -*-
from plone.app.contenttypes.behaviors.leadimage import ILeadImageBehavior
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets import ViewletBase
from zope.component import queryAdapter


class NoteLeadImageViewlet(ViewletBase):
    """Render the Note lead image in listing views.

    The stock ``contentleadimage`` viewlet only renders when the current
    view is the item's own ``IViewView``, so it is skipped when the item
    is rendered inside a collection or folder "All content" (full view)
    listing, where the current view is the listing view instead. This
    viewlet covers that case and stays out of the way on the item's own
    view, where the stock viewlet already renders the image.
    """

    def update(self):
        behavior = queryAdapter(self.context, ILeadImageBehavior)
        self.available = bool(behavior is not None and behavior.image)
        if IViewView.providedBy(self.view):
            self.available = False
