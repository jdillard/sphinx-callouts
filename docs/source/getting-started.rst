Getting Started
===============

This guide will help you get started with Sphinx Callouts, a Sphinx extension that adds support for callouts in your documentation.
Callouts allow you to annotate code examples with numbered references that correspond to detailed explanations below the code block.

What are Callouts?
------------------

Callouts are numbered annotations that help explain specific lines or sections of code. They consist of two required parts:

1. **Callout markers** - Numbers placed within the code at specific points (e.g., ``<1>``, ``<2>``)
2. **Callout annotations** - Explanatory text that corresponds to each numbered marker

This approach makes code examples more readable and educational by separating the code from lengthy explanations.

Basic Usage
-----------

The basic syntax uses the ``callout`` directive to wrap your code block, followed by an ``annotations`` directive to provide explanations:

.. code-block:: rst

    .. callout::

        .. code-block:: python

            def greet(name):  # <1>
                message = f"Hello, {name}!"  # <2>
                return message  # <3>

        .. annotations::
            :1: Define a function that takes a name parameter.
            :2: Create a formatted greeting message.
            :3: Return the message to the caller.

This renders as:

.. callout::

    .. code-block:: python

        def greet(name):  # <1>
            message = f"Hello, {name}!"  # <2>
            return message  # <3>

    .. annotations::
        :1: Define a function that takes a name parameter.
        :2: Create a formatted greeting message.
        :3: Return the message to the caller.

Using literalinclude
--------------------

For larger code examples, you can use ``literalinclude`` to include external files:

.. code-block:: rst

    .. callout::

        .. literalinclude:: examples.py
            :language: python
            :start-after: __quick_start_begin__
            :end-before: __quick_start_end__

        .. annotations::
            :1: Wrap a PyTorch model in an objective function that defines what we want to optimize.
            :2: Define a search space with different hyperparameter values to try. We use grid search for 'a' and choice for 'b'.
            :3: Start a Tune run that finds the configuration with the minimum score after testing all combinations.

Where ``examples.py`` is:

.. literalinclude:: examples.py

Which renders as:

.. callout::

    .. literalinclude:: examples.py
        :language: python
        :start-after: __quick_start_begin__
        :end-before: __quick_start_end__

    .. annotations::
        :1: Wrap a PyTorch model in an objective function that defines what we want to optimize.
        :2: Define a search space with different hyperparameter values to try. We use grid search for 'a' and choice for 'b'.
        :3: Start a Tune run that finds the configuration with the minimum score after testing all combinations.

Multi-Language Support
----------------------

Sphinx Callouts supports various comment styles for different programming languages:

.. callout::

    .. literalinclude:: examples.py
        :start-after: __multi_lang_begin__
        :end-before: __multi_lang_end__

    .. annotations::
        :1: Python uses hash (#) comments for callout markers.
        :2: C-style languages use double-slash (//) comments.
        :3: Clojure uses double-semicolon (;;) comments.
        :4: Erlang uses percent (%) comments.
        :5: SQL uses double-dash (--) comments.
        :6: Fortran uses exclamation (!) comments.
        :7: XML/HTML uses comment blocks (<!-- -->) for callouts.

Supported Comment Styles
~~~~~~~~~~~~~~~~~~~~~~~~~

The extension automatically recognizes these comment patterns:

.. list-table:: Supported Comment Styles
   :header-rows: 1
   :widths: 20 30 50

   * - Language
     - Comment Style
     - Example
   * - Python, Ruby, Bash, YAML
     - Hash
     - ``# <1>``
   * - JavaScript, C++, Java
     - Double slash
     - ``// <1>``
   * - Clojure, Lisp
     - Double semicolon
     - ``;; <1>``
   * - Erlang, MATLAB
     - Percent
     - ``% <1>``
   * - SQL, Lua
     - Double dash
     - ``-- <1>``
   * - Fortran
     - Exclamation
     - ``! <1>``
   * - XML, HTML
     - Comment block
     - ``<!--<1>-->``

Common Pitfalls
---------------

- **Mismatched numbers**: Make sure every ``<n>`` marker has a corresponding ``<n>`` annotation.
- **Comment syntax**: Use the correct comment style for your programming language.
- **Sequential numbering**: Avoid skipping numbers (don't jump from ``<1>`` to ``<3>``).

For more information, see the :doc:`contributing` guide or check out the project on GitHub.