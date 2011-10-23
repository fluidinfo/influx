"""Upload logic for easy importing into Fluidinfo."""

from json import load


class FluidinfoUploader(object):
    """A client that can read and upload structured data to Fluidinfo."""

    def uploadJSON(self, path):
        """Upload JSON data to Fluidinfo.

        @param path: The path to the file containing the data.
        """
        with open(path) as file:
            data = load(file)
        for batch in self._batchData(data):
            self._upload(batch)

    def _batchData(self, data):
        pass

    def _upload(self, data):
        pass


def splitObjects(data, batchSize=100):
    """Generator splits a C{dict} with information about objects into batches.

    @param data: A C{dict} with information about objects.
    @param batchSize: Optionally, the maximum number of objects to include in
        a batch.  Default is 100.
    @return: Generator yields a C{dict}, per iteration.
    """
    return
    yield
