# -*- coding: utf-8 -*-

from kaeru.note import _
from plone.dexterity.browser.view import DefaultView


# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class NoteView(DefaultView):
    # If you want to define a template here, please remove the template from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('note_view.pt')

    def __call__(self):
        # Implement your own actions:
        return super(NoteView, self).__call__()
