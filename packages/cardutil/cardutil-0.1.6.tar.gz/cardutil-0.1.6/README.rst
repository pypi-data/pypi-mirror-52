cardutil
========
Cardutil is a python package for working with payment card systems.

* Supports python 3.6 and later.
* The core library has **zero** package dependencies.
* Documentation available at  `readthedocs <https://cardutil.readthedocs.io/en/latest/>`_


.. image:: https://img.shields.io/pypi/l/cardutil.svg

.. image:: https://img.shields.io/pypi/v/cardutil.svg

.. image:: https://img.shields.io/pypi/wheel/cardutil.svg

.. image:: https://img.shields.io/pypi/implementation/cardutil.svg

.. image:: https://img.shields.io/pypi/status/cardutil.svg

.. image:: https://img.shields.io/pypi/dm/cardutil.svg

.. image:: https://img.shields.io/pypi/pyversions/cardutil.svg

.. image:: https://readthedocs.org/projects/cardutil/badge/?version=latest
   :target: https://cardutil.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

Quickstart
----------
Install
~~~~~~~
::

    $ pip install cardutil

ISO8583 messages
~~~~~~~~~~~~~~~~
Read an ISO8583 message returning dict::

    from cardutil import iso8583
    message_bytes = b'1144\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00164444555566667777'
    message_dict = iso8583.loads(message_bytes)

Create an ISO8583 message returning bytes::

    from cardutil import iso8583
    message_dict = {'MTI': '1144', 'DE2': '4444555566667777'}
    message_bytes = iso8583.dumps(message_dict)

Mastercard IPM files
~~~~~~~~~~~~~~~~~~~~
Read an IPM file::

    from cardutil import mciipm
    with open('ipm_in.bin', 'rb') as ipm_in:
        reader = mciipm.IpmReader(ipm_in)
        for record in reader:
            print(record)

Create an IPM file::

    from cardutil import mciipm
    with open('ipm_out.bin', 'wb') as ipm_out:
        writer = mciipm.IpmWriter(ipm_out)
        writer.write({'MTI': '1111', 'DE2': '9999111122221111'})
        writer.close()

cli tools
---------
.. note:: Not currently implemented.

The following command line interface tools are included in the package

* ``mci_ipm_extract`` converts Mastercard IPM files to csv
* ``mci_ipm_param_encode`` changes the encoding of a Mastercard IPM parameter files


Contributing
------------

install
~~~~~~~

::

    $ git clone https://bitbucket.org/hoganman/cardutil.git
    $ pip install -e ".[test]"

test
~~~~

::

    $ pytest

docs
~~~~

::

    $ pip install -e ".[docs]"
    $ make html -C ./docs
    $ open ./docs/build/html/index.html

release
~~~~~~~
.. note::
   Ensure that the source tree is clean before performing this process

::

    $ bumpversion (patch|minor|major)
    $ git push --follow-tags

acknowledgements
----------------
The python `hexdump` library is embedded in this package. Many thank to Anatoly Techtonik <techtonik@gmail.com>
This library is a life saver for debugging issues with binary data.
Available at `Pypi:hexdump <https://pypi.org/project/hexdump/>`_.

The python `ISO8583-Module` library was originally inspired by the work of Igor V. Custodio from his
original ISO8583 parser. Available at `Pypi:ISO8583-Module <https://pypi.org/project/ISO8583-Module/>`_.

Mastercard is a registered trademark of Mastercard International Incorporated.

