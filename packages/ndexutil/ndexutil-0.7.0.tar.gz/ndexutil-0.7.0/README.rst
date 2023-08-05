ndex-python-utilities
======================

**Warning: This repository is for development and features may change.
Please use this at your own risk.**

.. image:: https://img.shields.io/pypi/v/ndexutils.svg
        :target: https://pypi.python.org/pypi/ndexutils

.. image:: https://img.shields.io/travis/ndexbio/ndexutils.svg
        :target: https://travis-ci.org/ndexbio/ndexutils

.. image:: https://coveralls.io/repos/github/ndexbio/ndexutils/badge.svg?branch=master
        :target: https://coveralls.io/github/ndexbio/ndexutils?branch=master

.. image:: https://readthedocs.org/projects/ndexutils/badge/?version=latest
        :target: https://ndexutils.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

Dependencies
------------

* `ndex2 <https://pypi.org/project/ndex2>`_
* `networkx <https://pypi.org/project/networkx>`_
* `ndexutil <https://pypi.org/project/ndexutil>`_
* `biothings_client <https://pypi.org/project/biothings-client>`_
* `requests <https://pypi.org/project/requests>`_
* `requests-toolbelt <https://pypi.org/project/requests_toolbelt>`_
* `pandas <https://pypi.org/project/pandas>`_
* `mygene <https://pypi.org/project/mygene>`_
* `enum34 <https://pypi.org/project/enum34>`_
* `jsonschema <https://pypi.org/project/jsonschema>`_
* `urllib3 <https://pypi.org/project/urllib3>`_

Compatibility
-------------

* Python 3.5+

Installation
------------

.. code-block::

   git clone https://github.com/ndexbio/ndexutils
   cd ndexutils
   make dist
   pip install dist/ndexutil*whl

OR via `PyPI <https://pypi.org/ndexutils>`_

.. code-block::

   pip install ndexutil

ndexmisctools.py
-----------------

**WARNING:** Please consider this tool alpha and probably contains errors/bugs and could cause data corruption or loss. You have been warned

**ndexmisctools.py** lets caller perform some operations on NDEx via the
command line.
This tool follows format of ``ndexmisctools.py <COMMAND> <args>``

For more information run ``ndexmisctools.py --help`` and ``ndexmisctools.py <COMMAND> --help``

**COMMANDS**:

* **copynetwork** - copies NDEx network between accounts and even servers

  For copying the source and destination credentials must be stored in the configuration (default ``~/.ndexutils.conf``)
  and be formatted as follows:

  .. code-block::

   [mycopyprofile]
   source_user=bob
   source_password=6ea8f0ab0b2e
   source_server=public.ndexbio.org
   dest_user=smith
   dest_password=4efe9cd8
   dest_server=public.ndexbio.org

  The following command copies the network ``9025480b-6fbc-4efe-9cd8-b575ce49dfda`` from source credentials defined in configuration to dest

  .. code-block::

    ndexmisctools.py --profile mycopyprofile copynetwork --uuid 9025480b-6fbc-4efe-9cd8-b575ce49dfda


* **networkattribupdate** - updates network attributes on network in NDEx

  **WARNING:** Currently **name, version, and description** CANNOT be updated with this command.

  Credentials must be stored in the configuration (default ``~/.ndexutils.conf``)
  and be formatted as follows:

  .. code-block::

    [myattrib]
    user=bob
    password=6ea8f0ab0b2e
    server=public.ndexbio.org

  The following command updates **foo** network attribute on the network ``9025480b-6fbc-4efe-9cd8-b575ce49dfda``

  .. code-block::

    ndexmisctools.py --profile myattrib networkattribupdate --uuid 9025480b-6fbc-4efe-9cd8-b575ce49dfda --name foo --type string --value 'my new value'


* **systemproperty** - updates showcase, visibility, and indexing for single network or all networks in networkset in NDEx

  **NOTE:** ``--showcase`` has no effect if network visibility is ``private``

  Credentials must be stored in the configuration (default ``~/.ndexutils.conf``)
  and be formatted as follows:

  .. code-block::

    [myattrib]
    user=bob
    password=6ea8f0ab0b2e
    server=public.ndexbio.org

  The following command enables showcase and sets indexing to `meta` for network with id ``9025480b-6fbc-4efe-9cd8-b575ce49dfda``

  .. code-block::

    ndexmisctools.py --profile myattrib systemproperty --uuid 9025480b-6fbc-4efe-9cd8-b575ce49dfda --showcase --indexlevel meta

  The following command sets visibility to `public` for all networks in networkset with id ``e9580d43-ec14-4be8-9977-9de88e1d410a``

  .. code-block::

    ndexmisctools.py --profile myattrib systemproperty --networksetid e9580d43-ec14-4be8-9977-9de88e1d410a --visibility public


TSV Loader
----------

This module contains the Tab Separated Variable Loader (TSV Loader) which generates
an `NDEx CX <http://www.home.ndexbio.org/data-model/>`_ file from a tab separated
text file of edge data and attributes.

To load data a load plan must be created. This plan tells the loader how to map the
columns in the file to nodes, and edges. This load plan needs to validate against
`this load plan JSON schema <https://github.com/ndexbio/ndexutils/blob/master/ndexutil/tsv/loading_plan_schema.json>`_

**Example TSV file**

.. code-block::

    SOURCE  TARGET  WEIGHT
    ABCD    AAA1    0.555
    GGGG    BBBB    0.305

**SOURCE** is the source node, **TARGET** is target node

A schema that could be:

.. code-block::

    {
    "source_plan":
        {
            "node_name_column": "SOURCE"
        },
        "target_plan":
        {
            "node_name_column": "TARGET"
        },
        "edge_plan":
        {
            "default_predicate": "unknown",
            "property_columns": [
              {
                "column_name": "WEIGHT",
                "attribute_name": "weight",
                "data_type": "double"
              }
            ]
        }
    }



Example below assumes the following:

* **./loadplan.json** is the load plan in JSON format
* **./style.cx** is a `NDEx CX <http://www.home.ndexbio.org/data-model/>`_ with a style.

.. code-block::

    import ndex2
    from ndexutil.tsv.streamtsvloader import StreamTSVLoader

    # using ndex2 client library read CX file as NiceCXNetwork object
    style_network = ndex2.create_nice_cx_from_file('./style.cx')

    loader = StreamTSVLoader('./loadplan.json', style_network)
    with open('./input.tsv', 'r') as tsvfile:
        with open('./output.cx', 'w') as outfile:
            loader.write_cx_network(tsvfile, outfile)


Credits
-------

