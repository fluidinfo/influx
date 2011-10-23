from unittest import TestCase

from influx.client import FluidinfoImporter
from influx.tests.doubles import FakeFluidinfo


class FluidinfoImporterTest(TestCase):

    def testUploadEmptyDataset(self):
        """Uploading an empty dataset is a no-op."""
        fluidinfo = FakeFluidinfo()
        client = FluidinfoImporter(fluidinfo, 5)
        client.upload([])
        self.assertEqual([], fluidinfo.calls)

    def testUpload(self):
        """
        Object data is converted into a format compatible with the C{/values}
        API endoint and uploaded using the C{fluidinfo.py} client.
        """
        fluidinfo = FakeFluidinfo()
        client = FluidinfoImporter(fluidinfo, 5)
        client.upload([{'about': 'hello world', 'values': {'foo/bar': 13}}])
        body = {'queries': [['fluiddb/about = "hello world"',
                             {'foo/bar': {'value': 13}}]]}
        self.assertEqual([(('PUT', '/values', body), {})], fluidinfo.calls)
