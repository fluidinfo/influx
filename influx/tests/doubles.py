class FakeFluidinfo(object):
    """A fake C{fluidinfo.py} for use in unit tests."""

    def __init__(self):
        self.calls = []

    def call(self, *args, **kwargs):
        self.calls.append((args, kwargs))

