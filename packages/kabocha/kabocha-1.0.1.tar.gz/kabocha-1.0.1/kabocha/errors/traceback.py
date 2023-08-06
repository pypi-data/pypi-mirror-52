DEFAULT_TRACEBACK = "No traceback provided"

class TracebackMixin(object):
    def __init__(self, traceback=DEFAULT_TRACEBACK, **kwargs):
        super(TracebackMixin, self).__init__(**kwargs)
        self.traceback = traceback
    
    def traceback():
        doc = "String representation of Python tracebook. Defaults to '%s'" % DEFAULT_TRACEBACK

        def fget(self):
            return self.data['traceback']

        def fset(self, value):
            self.data['traceback'] = value
            self.update_content()

        def fdel(self):
            self.data['trackback'] = DEFAULT_TRACEBACK
            self.update_content()

        return locals()
    traceback = property(**traceback())