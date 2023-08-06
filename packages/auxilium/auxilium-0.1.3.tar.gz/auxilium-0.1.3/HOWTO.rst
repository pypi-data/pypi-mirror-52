
.. currentmodule:: auxilium


command option arguments
------------------------

All **auxilium** calls are expected to happen in project root directory.

.. code-block:: bash

        $ auxilium command -p=pre_run.sh
        . ./pre_run.sh;

will run the shell script :code:`pre_run.sh` before :code:`command`


.. code-block:: bash

        $ auxilium command ---VAR=VAL
        export VAR=VAL;

will set variable :code:`VAR` to :code:`VAL`.


create project function
-----------------------


.. code-block:: bash

    $ auxilium create

will create a project structure in current working directory.


pip functions
-------------

.. code-block:: bash

    $ auxilium setup
    *** setup environment requirements ***

will install via :code:`pip` additional packages as set by *requirements.txt* and *upgrade_requirements.txt*

.. code-block:: bash

    $ auxilium cleanup
    *** clean environment ***

removes temporary files and packages as set by *requirements.txt* and *upgrade_requirements.txt*


.. code-block:: bash

    $ auxilium install
    *** install project via pip install -e ***

installs current project in dev mode (*install -e*)


.. code-block:: bash

    $ auxilium uninstall
    *** uninstall project via pip uninstall ***

removes project via :code:`pip`


test and analysis functions
---------------------------

.. code-block:: bash

    $ auxilium test
    echo '*** run test scripts (opt. TEST_DIR=test)***';

runs unittests found in :code:`test`


.. code-block:: bash

    $ auxilium profile
    echo '*** run test profiling (opt. PROFILE_FILE=dev.py)***'

runs simple profiling of given file (default :code:`dev.py`)


.. code-block:: bash

    $ auxilium analysis
    echo '*** run code analysis scripts ***';
    echo '*** run pylint ***';
    echo '*** run bandit ***';

reviews code style and security with *pylint* and *bandit*


.. code-block:: bash

    $ auxilium coverage
    echo '*** run coverage scripts ***';

measures test coverage with *coverage.py*


doc functions
-------------

.. code-block:: bash

    $ auxilium api
    echo '*** run sphinx apidoc scripts ***';

extracts project structure from source code files


.. code-block:: bash

    $ auxilium html
    echo '*** run sphinx html scripts ***';

builds html documentation in :code:`doc/sphinx/_build/html`. Here :code:`index.html` can be found.


.. code-block:: bash

    $ auxilium latexpdf
    echo '*** run sphinx latexpdf scripts (req. latex installation)***';

builds html documentation in :code:`doc/sphinx/_build/latexpdf`. Here :code:`project.pdf` can be found.


.. code-block:: bash

    $ auxilium doctest
    echo '*** run sphinx doctest scripts ***';

runs doctest, i.e. testing code snips in doc strings


.. code-block:: bash

    $ auxilium sphinx
    echo '*** run sphinx scripts ***';

runs a combined script of doc tools: :code:`api; html; doctest;`


other functions
---------------

.. code-block:: bash

    $ auxilium build
    echo '*** run setuptools scripts ***';


.. code-block:: bash

    $ auxilium docmaintain
    echo '*** run docmaintain scripts ***';
    # release timestamp and file doc strings


github repo functions
---------------------

.. code-block:: bash

    $ auxilium repo
    echo '*** init a repository locally and on github.com (req. GITHUB_USR and GITHUB_PWD)***';


.. code-block:: bash

    $ auxilium release
    echo '*** draft release on github.com (req. GITHUB_USR and GITHUB_PWD)***';


pypi deploy functions
---------------------

.. code-block:: bash

    $ auxilium deploy
    echo '*** deploy release on pypi.org (req. PYPI_USR and PYPI_PWD)***';



test bundles
------------


.. code-block:: bash

    $ auxilium simple
    echo "*** run simple test pipeline ***"
    setup;
    run;


.. code-block:: bash

    $ auxilium full
    echo "*** run full test pipeline ***"
    setup;
    sphinx;
    analysis;
    codecoverage;
    build;
