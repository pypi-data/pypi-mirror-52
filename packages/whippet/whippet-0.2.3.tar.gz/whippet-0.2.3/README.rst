Whippet - like husky, but leaner
################################
A simple git hooks installer. Inspired by `husky <https://github.com/typicode/husky#readme>`_.

I liked simplicity of setting up git hooks using husky and since I failed to find a similar tool in python ecosystem, I
decided to write one myself.

As far as I know there is no standard equivalent to `npm scripts <https://docs.npmjs.com/misc/scripts>`_ in python, so I
chose to rely on `make <https://www.gnu.org/software/make/>`_ which seems to be a popular way to organise project
related tasks in python world.

Install
*******
Whippet is available as a `pypi package <https://pypi.org/project/whippet/>`_. Use a tool that can install packages from
it, like for instance `pip <https://pip.pypa.io/en/stable/>`_.

.. code-block:: bash

    $ pip install requests

Usage
*****
Once whippet is installed, it is used by invoking ``whippet`` executable in the directory where you wish to install
hooks. Whippet will check if that directory (or its ancestor) contains a ``.git`` directory and offer to install hooks
into it.

.. code-block:: bash

    $ cd demo
    $ whippet
    whippet - Are you sure you want to install hooks in /home/bpp/demo/.git? [Y/n] y

Whippet hooks are scripts that check for existence of make targets with the same name as git hooks. If such a target
exists, script will execute it. Let's take ``pre-commit`` as an example. Once whippet hooks are installed, we simply add
``pre-commit`` target to the Makefile like so:

.. code-block:: make

    pre-commit:
        @echo "Hello from whippet"


Then o
