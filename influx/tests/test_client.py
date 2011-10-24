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

    def testUploadEscapesDoubleQuotesInAboutValues(self):
        """
        Double quotes in about tag values are correctly escaped when converted
        to Fluidinfo queries.
        """
        fluidinfo = FakeFluidinfo()
        client = FluidinfoImporter(fluidinfo, 5)
        client.upload([{'about': '"hello world"', 'values': {'foo/bar': 13}}])
        body = {'queries': [[r'fluiddb/about = "\"hello world\""',
                             {'foo/bar': {'value': 13}}]]}
        self.assertEqual([(('PUT', '/values', body), {})], fluidinfo.calls)

    def testUploadLimitsByBatchSize(self):
        """
        Object data is split into batches, to control the number of objects
        that get added per request.
        """
        fluidinfo = FakeFluidinfo()
        client = FluidinfoImporter(fluidinfo, 1)
        client.upload([{'about': 'hello world', 'values': {'foo/bar': 13}}])
        client.upload([{'about': 'wubble', 'values': {'baz/quux': 42}}])
        body1 = {'queries': [['fluiddb/about = "hello world"',
                              {'foo/bar': {'value': 13}}]]}
        body2 = {'queries': [['fluiddb/about = "wubble"',
                              {'baz/quux': {'value': 42}}]]}
        self.assertEqual([(('PUT', '/values', body1), {}),
                          (('PUT', '/values', body2), {})], fluidinfo.calls)

    def testUploadMultipleObjects(self):
        """
        Objects are uploaded in batches when possible, depending on the batch
        size.
        """
        fluidinfo = FakeFluidinfo()
        client = FluidinfoImporter(fluidinfo, 2)
        client.upload([{'about': 'hello world', 'values': {'foo/bar': 13}},
                       {'about': 'wubble', 'values': {'baz/quux': 42}}])
        body = {'queries': [['fluiddb/about = "hello world"',
                             {'foo/bar': {'value': 13}}],
                            ['fluiddb/about = "wubble"',
                             {'baz/quux': {'value': 42}}]]}
        self.assertEqual([(('PUT', '/values', body), {})], fluidinfo.calls)

    def testUploadMultipleObjectsLimitsByBatchSize(self):
        """
        Objects are uploaded in batches when possible, depending on the batch
        size.
        """
        fluidinfo = FakeFluidinfo()
        client = FluidinfoImporter(fluidinfo, 2)
        client.upload([{'about': 'hello world', 'values': {'foo/bar': 13}},
                       {'about': 'wubble', 'values': {'baz/quux': 42}},
                       {'about': 'ooga', 'values': {'foo/bar': 67}}])
        body1 = {'queries': [['fluiddb/about = "hello world"',
                             {'foo/bar': {'value': 13}}],
                            ['fluiddb/about = "wubble"',
                             {'baz/quux': {'value': 42}}]]}
        body2 = {'queries': [['fluiddb/about = "ooga"',
                              {'foo/bar': {'value': 67}}]]}
        self.assertEqual([(('PUT', '/values', body1), {}),
                          (('PUT', '/values', body2), {})], fluidinfo.calls)
