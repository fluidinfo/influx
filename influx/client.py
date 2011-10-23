"""Upload logic for easy importing into Fluidinfo."""


class FluidinfoImporter(object):
    """Importer uploads data to Fluidinfo.

    @param client: The C{fluidinfo.py} instance to use to communicate with
        Fluidinfo.
    """

    def __init__(self, client, batchSize):
        self._client = client
        self._batchSize = batchSize

    def upload(self, objects):
        """Upload data to Fluidinfo.

        @param objects: A C{list} of C{dict}s representing tags and values,
            organized as objects, to upload to Fluidinfo.
        """
        start, end = 0, min(len(objects), self._batchSize)
        if end:
            while len(objects) >= start+end:
                self._upload(objects[start:end])
                start, end = end, min(len(objects), start + end)

    def _upload(self, objects):
        data = self._getValuesData(objects)
        self._client.call('PUT', '/values', data)

    def _getValuesData(self, objects):
        queries = []
        for objectData in objects:
            values = dict((key, {'value': value})
                          for key, value in objectData['values'].iteritems())
            queries.append(['fluiddb/about = "%s"' % objectData['about'],
                            values])
        if queries:
            return {'queries': queries}

