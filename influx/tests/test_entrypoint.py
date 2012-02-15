import httplib2
from unittest import TestCase

from influx.entrypoint import (
    MissingPathError, MissingPasswordError, MissingUsernameError,
    getFluidinfoClient, parseOptions)


class ParseOptionsTest(TestCase):

    def testParseOptionsWithoutValues(self):
        """A L{MissingPathError} is raised if no path is specified."""
        self.assertRaises(MissingPathError, parseOptions, [])

    def testParseOptionsWithoutUsername(self):
        """A L{MissingUsernameError} is raised if no username is specified."""
        self.assertRaises(MissingUsernameError, parseOptions,
                          ['-p', 'secret', 'path'])

    def testParseOptionsWithoutPassword(self):
        """A L{MissingPasswordError} is raised if no password is specified."""
        self.assertRaises(MissingPasswordError, parseOptions,
                          ['-u', 'user', 'path'])

    def testParseOptionsUsesSensibleDefaultValues(self):
        """Sensible defaults are provided for all options."""
        options, args = parseOptions(['-u', 'user', '-p', 'secret', 'path'])
        self.assertEqual(100, options.batchSize)
        self.assertEqual('https://fluiddb.fluidinfo.com', options.endpoint)
        self.assertFalse(options.verbose)
        self.assertEqual(['path'], args)

    def testParseOptions(self):
        """Command-line arguments override default values."""
        options, args = parseOptions(['-u', 'user', '-p', 'secret', '-b', '7',
                                      '-e', 'http://localhost:9000', 'path'])
        self.assertEqual('user', options.username)
        self.assertEqual('secret', options.password)
        self.assertEqual(7, options.batchSize)
        self.assertEqual('http://localhost:9000', options.endpoint)
        self.assertFalse(options.verbose)
        self.assertEqual(['path'], args)

    def testParseOptionsWithVerboseFlag(self):
        """An optional C{-v} flag can be provided to enable verbose logging."""
        options, args = parseOptions(['-u', 'user', '-p', 'secret', '-v',
                                      'path'])
        self.assertTrue(options.verbose)


class GetFluidinfoClientTest(TestCase):

    def testGetFluidinfoClientWithDefaultSettings(self):
        """The main instance is used by default."""
        options, args = parseOptions(['-u', 'user', '-p', 'secret', 'path'])
        client = getFluidinfoClient(options)
        self.assertEqual('https://fluiddb.fluidinfo.com', client.instance)
        self.assertEqual('Basic dXNlcjpzZWNyZXQ=',
                         client.global_headers['Authorization'])

    def testGetFluidinfoClientWithCustomSettings(self):
        """
        The API endpoint can be configured by passing a command-line argument.
        """
        options, args = parseOptions(['-u', 'user', '-p', 'secret',
                                      '-e', 'http://localhost:9000', 'path'])
        client = getFluidinfoClient(options)
        self.assertEqual('http://localhost:9000', client.instance)
        self.assertEqual('Basic dXNlcjpzZWNyZXQ=',
                         client.global_headers['Authorization'])

    def testGetFluidinfoClientWithVerboseFlag(self):
        """Debugging is enabled in C{httplib2} when the verbose flag is set."""
        originalDebugLevel = httplib2.debuglevel
        try:
            options, args = parseOptions(['-u', 'user', '-p', 'secret',
                                          '-e', 'http://localhost:9000', '-v',
                                          'path'])
            getFluidinfoClient(options)
            self.assertEqual(1, httplib2.debuglevel)
        finally:
            httplib2.debuglevel = originalDebugLevel
