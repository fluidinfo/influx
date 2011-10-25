class FakeFluidinfo(object):
    """A fake C{fluidinfo.py} for use in unit tests."""

    def __init__(self):
        self.calls = []

    def call(self, *args, **kwargs):
        """Invoke an API method.  See C{fluidinfo.py} for details.

        The positional and keyword arguments passed to this method are stored
        in a C{calls} list.  It can be inspected by test logic to determine
        whether the expected calls were made.
        """
        self.calls.append((args, kwargs))
