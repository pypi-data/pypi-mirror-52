 \* \* * # Rkhunter Installer * \* \*

Summary
-------

Utility for installing and configuring the latest version of `Rkhunter
Malware Scanner <https://en.wikipedia.org/wiki/Rkhunter>`__ for linux.

Rkhunter Installer, version **1.7**

--------------

Contents
--------

-  `Getting Started <#getting-started>`__
-  `Scope <#scope>`__
-  `Dependencies <#dependencies>`__
-  `Instructions <#instructions>`__
-  `Help <#help>`__
-  `Author & Copyright <#author--copyright>`__
-  `License <#license>`__
-  `Disclaimer <#disclaimer>`__

--------------

Getting Started
---------------

See the following resources before getting started:

-  Rkhunter `Project Site <http://rkhunter.sourceforge.net/>`__ on
   Sourceforge
-  Rkhunter Official
   `README <https://sourceforge.net/p/rkhunter/rkh_code/ci/master/tree/files/README>`__

`back to the top <#top>`__

--------------

Scope
-----

rkhunter-install will perform the following on your system to satisfy
Rkhunter dependencies:

-  **Perl Modules**:

   -  Installation of ``cpan`` if required
   -  Installation of Perl module dependencies that rkhunter uses for
      malware or other checks

-  **C Library**: ``unhide``

   -  required for discovery of hidden processes
   -  compiles, installs

-  **C Library**: ``skdet``

   -  required for specialized rootkit detection
   -  compiles, installs

-  **Uninstall Utility**

   -  Installs uninstall utility in local config directory should you
      ever need to remove Rkhunter

-  **Configuration File**

   -  generates local configuration file required for uninstall

`back to the top <#top>`__

--------------

Dependencies
------------

-  Ubuntu, Ubuntu variants, 14.04
-  Ubuntu, Ubuntu variants, 16.04+
-  Redhat, Centos v7.0+
-  `Amazon Linux <https://aws.amazon.com/amazon-linux-ami>`__ 2017+
-  Installation of required fonts (``ttf-mscorefonts-installer``)

`back to the top <#top>`__

--------------

Instructions
------------

Run the installer from the cli via the following command:

.. code:: bash

        $ sudo sh rkhunter-install.sh

Installation directory is set using the ``--layout`` parameter:

.. code:: bash


        $ sudo sh rkhunter-install.sh --layout /usr    

            # install directory /usr/bin

If the ``--layout`` parameter is not provided, the following is assumed:

.. code:: bash


        $ sudo sh rkhunter-install.sh --layout "default"    

            # install directory /usr/local/bin

**NOTE**: \* Root privileges (sudo) must be used or run the installer
directly as root \* The installer performs an integrity check using
sha256 on all files it retrieves. The installation will only proceed if
integrity check passes.

`back to the top <#top>`__

--------------

Help
----

To display the help menu:

.. code:: bash

        $ sh rkhunter-install.sh --help

|help|

To display help menu for the ``--configure`` option:

.. code:: bash

        $ sh rkhunter-install.sh --configure

|help-configure|

`back to the top <#top>`__

--------------

Author & Copyright
------------------

All works contained herein copyrighted via below author unless work is
explicitly noted by an alternate author.

-  Copyright Blake Huber, All Rights Reserved.

`back to the top <#top>`__

--------------

License
-------

-  Software contained in this repo is licensed under the `license
   agreement <./LICENSE.md>`__.

`back to the top <#top>`__

--------------

Disclaimer
----------

*Code is provided "as is". No liability is assumed by either the code's
originating author nor this repo's owner for their use at AWS or any
other facility. Furthermore, running function code at AWS may incur
monetary charges; in some cases, charges may be substantial. Charges are
the sole responsibility of the account holder executing code obtained
from this library.*

Additional terms may be found in the complete `license
agreement <./LICENSE.md>`__.

`back to the top <#top>`__

--------------

`back to repository README <../README.md>`__

.. |help| image:: ./assets/help-menu.png
   :target: https://rawgithub.com/fstab50/gensec/master/rkhunter/assets/help-menu.png
.. |help-configure| image:: ./assets/help-configure.png
   :target: https://rawgithub.com/fstab50/gensec/master/rkhunter/assets/help-configure.png
