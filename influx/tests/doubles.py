class FakeResponse(object):
    """A fake C{httplib2.Response} object for use in unit tests."""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class FakeFluidinfo(object):
    """A fake C{fluidinfo.py} for use in unit tests.

    @param responses: Optionally, a list of C{(FakeResponse, content)}
        2-tuples to return when calls are made.  2-tuples will be popped from
        the front of the list for each call.  If no data is available a
        successful L{FakeResponse} with a C{None} content body will be
        returned.
    """

    def __init__(self, responses=None):
        self.calls = []
        self.responses = responses if responses else []

    def call(self, *args, **kwargs):
        """Invoke an API method.  See C{fluidinfo.py} for details.

        The positional and keyword arguments passed to this method are stored
        in a C{calls} list.  It can be inspected by test logic to determine
        whether the expected calls were made.
        """
        self.calls.append((args, kwargs))
        if self.responses:
            return self.responses.pop(0)
        return FakeResponse(reason='Ok', status=200), None
