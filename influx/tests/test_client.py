from unittest import TestCase

from influx.client import FluidinfoUploader, splitObjects


class FluidinfoUploaderTest(TestCase):

    def testUploadJSONWithMissingFile(self):
        """An C{IOError} is raised if the specified JSON file doesn't exist."""
        client = FluidinfoUploader()
        self.assertRaises(IOError, client.uploadJSON, '/foo/bar/baz')


class SplitObjectsTest(TestCase):

    def testSplitObjectsWithoutData(self):
        """No values are returned if no data is provided."""
        self.assertEqual([], list(splitObjects({})))
