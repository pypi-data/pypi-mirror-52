# -*- coding: utf-8 -*-

"""
Created on 2016-07-01
:author: Oshane Bailey (b4.oshany@gmail.com)
"""


class BaseView(object):
    """ Base class for views """

    def __init__(self, context, request):
        """ Constructor

        :param context: Context of the view
        :type context: :class:`kotti.resources.Content`

        :param request: Current request
        :type request: :class:`kotti.request.Request`
        """

        super(BaseView, self).__init__()

        self.context = context
        self.request = request
