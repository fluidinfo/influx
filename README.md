Influx is a simple tool for importing datasets into Fluidinfo.


Introduction
------------

Uploading large amounts of data to Fluidinfo is relatively easy, but
also mundane, and there is a lot of repetition of logic when scripts
are hand-written for different datasets.  Influx attempts to remove as
much work as possible from the process by defining a common data
format for representing datasets to be imported into Fluidinfo and
providing a simple tool to upload that data.


Installation
------------

Create a virtualenv and install the requirements:

    virtualenv --no-site-packages env
    . env/bin/activate
    pip install -r requirements.txt


Data format
-----------

The data to be uploaded must be provided in the following JSON format:

    {'objects': [{'about': <about-tag-value>,
                  'values': {<tag-path>: <tag-value>, ...}},
                 ...]
    }

This data will be loaded into memory, so it's important to make sure
the JSON data structure doesn't get too big.  For very large datasets,
it's best to split the data into multiple files.  The following
example contains two objects that represent the Anarchism and Autism
pages in Wikipedia.  Each object has an about tag and a single
`en.wikipedia.org/url` tag value:

    {"objects": [
        {"about": "anarchism",
         "values": {
             "en.wikipedia.org/url": "http://en.wikipedia.org/wiki/Anarchism"}},
        {"about": "autism",
         "values": {
             "en.wikipedia.org/url": "http://en.wikipedia.org/wiki/Autism"}}]
    }


Uploading data
--------------

In the simplest case, a dataset is represented in a single file.  You
need to pass a username and password and specify the file:

    bin/influx -u username -p password data.json

Infux will load the file, upload it to Fluidinfo and print status
information as it goes.  If you have many files you can pass them as
arguments to Influx:

    bin/influx -u username -p password data1.json data2.json data3.json

You can also specify a directory, in which case Influx will load and
upload all files that end with `.json`:

    bin/influx -u username -p password directory

You can mix and match directories and filenames, as you wish.


Using a different API endpoint
------------------------------

You can provide a custom API endpoint, to upload data to the sandbox,
for example:

    bin/influx -u username -p password -e http://endpoint data.json


Customizing the batch size
--------------------------

When Influx loads the data from the JSON files you specify it uploads
them in batches.  The default is a good choice for most datasets, but
you might get better performance with a different value.  You can
specify the batch size on the command-line:

    bin/influx -u username -p password -b 75 data.json


Debugging
---------

When you need to debug an issue you can use `-v` to enable verbose
mode which writes details out about requests as they happen:

    bin/influx -u username -p password -v data.json
