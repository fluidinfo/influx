Influx is an import tool for Fluidinfo.


Overview
--------

Uploading large amounts of data to Fluidinfo is relatively easy, but
also mundane, and there is a lot of repetition of logic when scripts
are hand-written for different datasets.  Influx attempts to remove as
much work as possible from the process by defining a common data
format for representing data to be imported into Fluidinfo and
providing tools to upload that data.

The data to be uploaded must be provided in the following JSON format:

    {'objects': [{'about': <about-tag-value>,
                  'values': [{<tag-path>: <tag-value>, ...},
                              ...]},
                 {'id': <object-id>,
                  'values': [{<tag-path>: <tag-value>, ...},
                              ...]},
                 {'query': <query-string>,
                  'values': [{<tag-path>: <tag-value>, ...},
                              ...]},
                 ...]
    }

This data will be loaded into memory, so it's important to make sure
the JSON data structure doesn't get too big.  For very large datasets,
it's best to split the data into multiple files, which can then be
passed to the `influx` tool.
