|image0| |image2| |image3| |PyPI - Python Version|

jootranslate
------------

Searches for JText::\_ translations in php files and generates the ini
files. If the file exist only new translation strings will be added.

This is just a little helper so you don\`t have to copy and paste all
your translation strings by hand.

Your component needs the following directory structure

::

    admin
        - controllers
        - language
        - etc ...
    site
        - controllers
        - language
        - etc...

**installation**

use pip

::

    pip install jootranslate

local

::

    python setup.py install

**usage**

::

    jootranslate --source /path/to/component/root --com your_component

to see a full list of all options

::

    jootranslate -h

**todo**

Parse the xml files for translations and generate the \*.sys.ini files

.. |image0| image:: https://img.shields.io/pypi/v/jootranslate.svg
   :target: https://pypi.python.org/pypi?name=jootranslate&:action=display
.. |image2| image:: https://pyup.io/repos/github/pfitzer/jtranslate/shield.svg?t=1520427395490
   :target: https://pyup.io/account/repos/github/pfitzer/jtranslate/
.. |image3| image:: https://pyup.io/repos/github/pfitzer/jtranslate/python-3-shield.svg?t=1520427395491
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/jootranslate.svg
   :target: https://pypi.python.org/pypi?name=jootranslate&:action=display
