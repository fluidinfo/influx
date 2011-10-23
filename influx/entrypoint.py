"""Entry point for the Influx import tool."""

from optparse import OptionParser


class MissingPathError(Exception):
    """Raised if no file path is provided when the C{influx} tool is run."""


def main(args):
    """Run the Influx import tool.

    @param args: A C{list} of command-line arguments, typically C{sys.argv}.
    """
    options, args = parseOptions(args)
    importer = FluidinfoImporter()


def parseOptions(args):
    """Parse command-line options.

    @param args: The command-line arguments passed to the program.
    @raise MissingPathError: Raised if no file path argument is provided.
    @return: An C{(options, args)} 2-tuple.
    """
    parser = OptionParser()
    parser.usage = 'influx [options] PATH...'
    parser.add_option('-b', dest='batchSize', metavar='BATCH_SIZE', type=int,
                      help='number of objects to upload per batch '
                           '(default is 100)', default=100)
    (options, args) = parser.parse_args(args)
    if not args:
        raise MissingPathError('At least one path must be provided.')
    return options, args
