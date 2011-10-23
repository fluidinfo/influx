from unittest import TestCase

from influx.entrypoint import MissingPathError, parseOptions


class ParseOptionsTest(TestCase):

    def testParseOptionsWithoutValues(self):
        """A L{MissingPathError} is raised if no path is specified."""
        self.assertRaises(MissingPathError, parseOptions, [])

    def testParseOptionsUsesSensibleDefaultValues(self):
        """Sensible defaults are provided for all options."""
        options, args = parseOptions(['path'])
        self.assertEqual(100, options.batchSize)
        self.assertEqual('https://fluiddb.fluidinfo.com', options.endpoint)
        self.assertEqual(['path'], args)

    def testParseOptions(self):
        """Command-line arguments override default values."""
        options, args = parseOptions(
            ['-b', '7', '-e', 'http://localhost:9000', 'path'])
        self.assertEqual(7, options.batchSize)
        self.assertEqual('http://localhost:9000', options.endpoint)
        self.assertEqual(['path'], args)
