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
        @raises RuntimeError: Raised if a request is not successful.
        """
        start, end = 0, min(len(objects), self._batchSize)
        if end:
            while start < len(objects):
                data = self._getValuesData(objects[start:end])
                response, content = self._client.call('PUT', '/values', data)
                if response.status >= 300:
                    raise RuntimeError('Got status %d with content: %s'
                                       % (response.status, content))
                start, end = end, min(len(objects), end + self._batchSize)

    def _getValuesData(self, objects):
        """Convert the Influx object data format into the C{/values} format.

        @param objects: The C{list} of objects to convert into the C{/values}
            format.
        @return: A C{dict} with object information that can be used to make a
            C{/values} request.
        """
        queries = []
        for objectData in objects:
            values = dict((key, {'value': value})
                          for key, value in objectData['values'].iteritems())
            aboutValue = objectData['about'].replace('"', r'\"')
            queries.append(['fluiddb/about = "%s"' % aboutValue,
                            values])
        return {'queries': queries}
