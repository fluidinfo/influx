from unittest import TestCase

from influx.entrypoint import MissingPathError, parseOptions


class ParseOptionsTest(TestCase):

    def testParseOptionsWithoutValues(self):
        """A L{MissingPathError} is raised if no path is specified."""
        self.assertRaises(MissingPathError, parseOptions, [])

    def testParseOptions(self):
        """
        A C{(options, args)} 2-tuple is returned when arguments have been
        parsed.
        """
        options, args = parseOptions(['-b', '7', 'path'])
        self.assertEqual(7, options.batchSize)
        self.assertEqual(['path'], args)
