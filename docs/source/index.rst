Sphinx Callouts
===============

A `Sphinx`_ extension that adds support for callouts.

|PyPI version| |Downloads| |Parallel Safe| |GitHub Stars|

Installation
------------

Directly install via ``pip`` by using:

.. code-block:: bash

    pip install sphinx-callouts

Usage
-----

Add the extension to your Sphinx configuration (``conf.py``):

.. code-block:: python

    extensions = [
        'sphinx_callouts',
    ]

Example
-------

.. callout::

    .. literalinclude:: example.py
        :language: python
        :start-after: __quick_start_begin_
        :end-before: __quick_start_end__

    .. annotations::
        <1> Wrap a PyTorch model in an objective function.

        <2> Define a search space and initialize the search algorithm.

        <3> Start a Tune run that maximizes mean accuracy and stops after 5 iterations.

Multi-Language Comment Support
------------------------------

.. callout::

    .. literalinclude:: multi_language_example.py
        :language: python
        :start-after: __multi_lang_begin__
        :end-before: __multi_lang_end__

    .. annotations::
        <1> Python hash comment style.

        <2> C-style double-slash comment.

        <3> Clojure double-semicolon comment.

        <4> Erlang percent comment.

        <5> SQL double-dash comment.

        <6> Fortran exclamation comment.

        <7> XML/HTML comment style.

.. toctree::
   :maxdepth: 2

   contributing
   changelog


.. _Sphinx: http://sphinx-doc.org/

.. |PyPI version| image:: https://img.shields.io/pypi/v/sphinx-callouts.svg
   :target: https://pypi.python.org/pypi/sphinx-callouts
   :alt: Latest PyPi Version
.. |Downloads| image:: https://static.pepy.tech/badge/sphinx-callouts/month
    :target: https://pepy.tech/project/sphinx-callouts
    :alt: PyPi Downloads per month
.. |Parallel Safe| image:: https://img.shields.io/badge/parallel%20safe-true-brightgreen
   :target: #
   :alt: Parallel read/write safe
.. |GitHub Stars| image:: https://img.shields.io/github/stars/jdillard/sphinx-callouts?style=social
   :target: https://github.com/jdillard/sphinx-callouts
   :alt: GitHub Repository stars
