"""Entry point for the Influx import tool."""

from json import load
import logging
from optparse import OptionParser

import fluidinfo

from influx.client import FluidinfoImporter


class MissingPathError(Exception):
    """Raised if no file path is provided when the C{influx} tool is run."""


class MissingUsernameError(Exception):
    """Raised if no username is provided when the C{influx} tool is run."""


class MissingPasswordError(Exception):
    """Raised if no password is provided when the C{influx} tool is run."""


def main(args):
    """Run the Influx import tool.

    @param args: A C{list} of command-line arguments, typically C{sys.argv}.
    """
    options, args = parseOptions(args)
    client = getFluidinfoClient(options)
    importer = FluidinfoImporter(client, options.batchSize)
    logging.basicConfig(format='%(asctime)s %(levelname)8s  %(message)s',
                        level=logging.INFO)
    for path in args:
        with open(path, 'r') as file:
            data = load(file)
            logging.info('Uploading objects from %s' % path)
            importer.upload(data['objects'])


def parseOptions(args):
    """Parse command-line options.

    @param args: The command-line arguments passed to the program.
    @raise MissingPathError: Raised if no file path argument is provided.
    @return: An C{(options, args)} 2-tuple.
    """
    parser = getOptionParser()
    options, args = parser.parse_args(args)
    if not args:
        raise MissingPathError('At least one path must be provided.')
    if not options.username:
        raise MissingUsernameError('You must provide a username (see -u).')
    if not options.password:
        raise MissingPasswordError('You must provide a username (see -u).')
    return options, args


def getFluidinfoClient(options):
    """Configure and return a C{fluidinfo.py} client for use with Fluidinfo.

    @param options: An C{optparse.Values} instance with options loaded from
        the command-line.
    @return: A ready-to-use C{fluidinfo.py} instance.
    """
    fluidinfo.instance = options.endpoint
    fluidinfo.login(options.username, options.password)
    return fluidinfo


def getOptionParser():
    """Build an C{OptionParser} for the Influx tool.

    @return: A ready-to-use C{OptionParser} instance.
    """
    parser = OptionParser()
    parser.usage = 'influx [options] PATH...'
    parser.add_option('-b', dest='batchSize', metavar='BATCH_SIZE', type=int,
                      help='The maximum number of objects to upload per batch '
                           '(default is 100)', default=100)
    parser.add_option('-e', dest='endpoint', metavar='URL',
                      help='The API endpoint to use (default is '
                           'https://fluiddb.fluidinfo.com)',
                      default='https://fluiddb.fluidinfo.com')
    parser.add_option('-u', dest='username', metavar='USERNAME',
                      help='The Fluidinfo username to use when making API '
                           'calls')
    parser.add_option('-p', dest='password', metavar='PASSWORD',
                      help='The Fluidinfo password to use when making API '
                           'calls')
    return parser
