 \* \* * # xlines * \* \*

Summary
-------

Count the number of lines of text in a code project (or anything else)

**Version**: 0.7.8

--------------

Contents
--------

-  `**Dependencies** <#dependencies>`__

-  `**Program Options** <#program-options>`__

-  `**Build Options** <#build-options>`__

-  `**Configuration** <#configuration>`__

-  `**Exclusions** <#exclusions>`__

-  `**Installation** <#installation>`__

   -  `Pip Install <#installation>`__
   -  `Ubuntu, Linux Mint, Debian-based
      Distributions <#debian-distro-install>`__
   -  `Redhat, CentOS, Fedora <#redhat-distro-install>`__
   -  `Amazon Linux 2 <#amzn2-distro-install>`__

-  `**Screenshots** <#screenshots>`__

-  `**Author & Copyright** <#author--copyright>`__

-  `**License** <#license>`__

-  `**Disclaimer** <#disclaimer>`__

--

`back to the top <#top>`__

--------------

Dependencies
------------

`xlines <https://github.com/fstab50/xlines>`__ requires `Python
3.6+ <https://docs.python.org/3/>`__.

If your environment has Python 3.5 or older or is missing Python 3
altogether, consider using nlines as an excellent alternative. nlines
`bash <https://www.gnu.org/software/bash>`__ implementation line counter
is compatible with virtually any Linux-based development environment.

`back to the top <#top>`__

--------------

Program Options
---------------

To display the **xlines** help menu:

.. code:: bash

        $ xlines --help

.. raw:: html

   <p align="center">

::

    <a href="http://images.awspros.world/xlines/help-menu.png" target="_blank"><img src="./assets/help-menu.png">

.. raw:: html

   </p>

--

`back to the top <#top>`__

--------------

Build options
-------------

**`GNU Make <https://www.gnu.org/software/make>`__ Targets**. Type the
following to display the available make targets from the root of the
project:

.. code:: bash

        $  make help

.. raw:: html

   <p align="center">

::

    <a href="http://images.awspros.world/xlines/make-help.png" target="_blank"><img src="./assets/make-help.png">

.. raw:: html

   </p>

--

`back to the top <#top>`__

--------------

Configuration
-------------

Configure `xlines <https://github.com/fstab50/xlines>`__ runtime options
by entering the configuration menu:

.. code:: bash

        $ xlines --configure

|toc| 

`back to the top <#top>`__

--

Option "A" (shown below) allows addition of file types to be excluded
(skipped) from line totals

|option a|

`back to the top <#top>`__

--

Option "B" (shown below) allows deletion of file types from the
exclusion list so that a specific file extension will be included in
total line counts:

|option b| 

`back to the top <#top>`__

--

Option "C" (shown below) allows user-customization of files highlighted
for containing a large number of lines of text:

|option c|

--

`back to the top <#top>`__

--------------

Installation
------------

--------------

Pip Install
~~~~~~~~~~~

**xlines** may be installed on Linux via `pip, python package
installer <https://pypi.org/project/pip>`__ in one of two methods:

To install **xlines** for a single user:

::

    $  pip3 install xlines --user

To install **xlines** for all users (Linux):

::

    $  sudo -H pip3 install xlines

`back to the top <#top>`__

--------------

 ### Ubuntu, Linux Mint, Debian variants

**xlines** is not yet offered in native Debian Linux package format.

`back to the top <#top>`__

--------------

 ### Redhat, CentOS, Fedora

The easiest way to install **xlines** on redhat-based Linux
distributions is via the developer-tools package repository:

1. Install the official epel package repository

   ::

       $ sudo yum install epel-release

2. Download and install the repo definition file

   ::

       $ sudo yum install wget

   |rpm-install1|

   ::

       $ wget http://awscloud.center/rpm/developer-tools.repo

   |rpm-install2|

   ::

       $ sudo chown 0:0 developer-tools.repo && sudo mv developer-tools.repo /etc/yum.repos.d/

3. Update local repository cache

   ::

       $ sudo yum update -y

4. Install **xlines** os package

   ::

       $ sudo yum install xlines

   |rpm-install3|

   Answer "y":

   |rpm-install4|

5. Verify Installation

   ::

       $ yum info xlines

   |rpm-install5|

`back to the top <#top>`__

--------------

 ### Amazon Linux 2

The easiest way to install **xlines** on redhat-based Linux distribution
Amazon Linux 2, is via the developer-tools
`amzn2.awscloud.center <http://amzn2.awscloud.center>`__ package
repository:

1. Install the official epel package repository

   ::

       $ sudo amazon-linux-extras install epel -y

2. Download and install the repo definition file

   ::

       $ sudo yum install wget

   |rpm-install1|

   ::

       $ wget http://awscloud.center/amzn2/developer-tools.repo

   |rpm-install2|

   ::

       $ sudo chown 0:0 developer-tools.repo && sudo mv developer-tools.repo /etc/yum.repos.d/

3. Update local repository cache

   ::

       $ sudo yum update -y

4. **IMPORTANT**: Prior to installing **xlines**, verify the python3
   version installed.

   -  If Python 3.6 is installed, *installing xlines will install Amazon
      Linux 2 base python3, which is Python 3.7*.
   -  This change should not have any effect on the OS support
      applications themselves.
   -  You should evaluate the small chance that there is a potential
      effect on custom applications running on the machine.

5. Install **xlines** os package

   ::

       $ sudo yum install xlines

   |rpm-install3|

   Answer "y":

   |rpm-install4|

6. Verify Installation

   ::

       $ yum info xlines

   |rpm-install5|

   A check of python3 should point to Python 3.7:

   ::

       $ python3 --version

   ::

       $ Python 3.7.X

--

`back to the top <#top>`__

--------------

Screenshots
-----------

Counting lines in large repository with long paths.

.. code:: bash

        $ xlines  --sum  git/AWSAMPLES/aws-serverless-workshops/

.. raw:: html

   <p align="center">

::

    <a href="http://images.awspros.world/xlines/xlines_output_large.png"><img src="./assets/xlines-output-md.png" width="900">

.. raw:: html

   </p>

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
   agreement <./LICENSE.md>`__. You may display the license and
   copyright information by issuing the following command:

::

    $ xlines --version

|help|

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

.. |toc| image:: ./assets/configure_toc.png
   :target: http://images.awspros.world/xlines/configure_toc.png
.. |option a| image:: ./assets/configure_a.png
   :target: http://images.awspros.world/xlines/configure_a.png
.. |option b| image:: ./assets/configure_b.png
   :target: http://images.awspros.world/xlines/configure_b.png
.. |option c| image:: ./assets/configure_c.png
   :target: http://images.awspros.world/xlines/configure_c.png
.. |rpm-install1| image:: ./assets/rpm-install-1.png
   :target: http://images.awspros.world/xlines/rpm-install-1.png
.. |rpm-install2| image:: ./assets/rpm-install-2.png
   :target: http://images.awspros.world/xlines/rpm-install-2.png
.. |rpm-install3| image:: ./assets/rpm-install-3.png
   :target: http://images.awspros.world/xlines/rpm-install-3.png
.. |rpm-install4| image:: ./assets/rpm-install-4.png
   :target: http://images.awspros.world/xlines/rpm-install-4.png
.. |rpm-install5| image:: ./assets/rpm-install-5.png
   :target: http://images.awspros.world/xlines/rpm-install-5.png
.. |help| image:: ./assets/version-copyright.png
   :target: https://s3.us-east-2.amazonaws.com/http-imagestore/xlines/version-copyright.png
