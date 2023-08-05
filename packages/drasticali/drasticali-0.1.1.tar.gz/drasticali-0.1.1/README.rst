==========
drasticali
==========

|Pypi Version|
|Build Version|
|Python Versions|
|Project License|

Diverse Radio Astronomy Software Tools for Imaging and Calibration

Main website: DRASTICALI_

==============
Introduction
==============

Radio astronomy reduction tools for the next generation radio telescope.

==============
Installation
==============

Installation from source_,
working directory where source is checked out

.. code-block:: bash
  
    $ pip install .

This package is available on *PYPI*, allowing

.. code-block:: bash
  
    $ pip install drasticali

Then pull and/or build stimela images

**uDocker** [Recommended]

.. code-block:: bash

    $ stimela pull

**Podman** [Recommended]

.. code-block:: bash

    $ stimela pull -p

**Singularity** [Recommeded]

.. code-block:: bash

     $ stimela pull --singularity --pull-folder <folder to store stimela singularity images>

**Docker**

.. code-block:: bash

     $ stimela pull -d
     $ stimela build

=======
License
=======

This project is licensed under the GNU General Public License v3.0 - see license_ for details.

=============
Contribute
=============

Contributions are always welcome! Please ensure that you adhere to our coding
standards pep8_.

.. |Pypi Version| image:: https://img.shields.io/pypi/v/drasticali.svg
                  :target: https://pypi.python.org/pypi/drasticali
                  :alt:
.. |Build Version| image:: https://travis-ci.org/Athanaseus/drasticali.svg?branch=master
                  :target: https://travis-ci.org/Athanaseus/drasticali
                  :alt:

.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/drasticali.svg
                     :target: https://pypi.python.org/pypi/drasticali/
                     :alt:

.. |Project License| image:: https://img.shields.io/badge/license-GPL-blue.svg
                     :target: https://github.com/Athanaseus/drasticali/blob/master/LICENSE
                     :alt:

.. _DRASTICALI: https://github.com/Athanaseus/drasticali/wiki
.. _source: https://github.com/Athanaseus/drasticali
.. _license: https://github.com/Athanaseus/drasticali/blob/master/LICENSE
.. _pep8: https://www.python.org/dev/peps/pep-0008
