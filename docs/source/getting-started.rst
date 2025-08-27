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
            <1> Define a function that takes a name parameter.
            <2> Create a formatted greeting message.
            <3> Return the message to the caller.

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

Example 1: Basic Machine Learning Tutorial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. callout::

    .. literalinclude:: example.py
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

    .. literalinclude:: multi_language_example.py
        :language: python
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
   * - Python, Ruby, Bash
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

Advanced Examples
-----------------

Example 2: Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. callout::

    .. code-block:: yaml

        # Database configuration
        database:  # <1>
          host: localhost  # <2>
          port: 5432  # <3>
          name: myapp  # <4>

        # Redis configuration
        redis:  # <5>
          host: localhost
          port: 6379

    .. annotations::
        :1: Database section contains all database-related settings.
        :2: The hostname where the database server is running.
        :3: Port number for database connections (PostgreSQL default).
        :4: Name of the database to connect to.
        :5: Redis section for caching configuration.

Example 3: Docker Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. callout::

    .. code-block:: dockerfile

        FROM python:3.9-slim  # <1>

        WORKDIR /app  # <2>

        COPY requirements.txt .  # <3>
        RUN pip install -r requirements.txt  # <4>

        COPY . .  # <5>

        EXPOSE 8000  # <6>
        CMD ["python", "app.py"]  # <7>

    .. annotations::
        :1: Use Python 3.9 slim image as the base image.
        :2: Set the working directory inside the container.
        :3: Copy the requirements file to leverage Docker layer caching.
        :4: Install Python dependencies.
        :5: Copy the rest of the application code.
        :6: Expose port 8000 for the web application.
        :7: Define the command to run when the container starts.

Common Pitfalls
---------------

- **Mismatched numbers**: Make sure every ``<n>`` marker has a corresponding ``<n>`` annotation.
- **Comment syntax**: Use the correct comment style for your programming language.
- **Sequential numbering**: Avoid skipping numbers (don't jump from ``<1>`` to ``<3>``).

For more information, see the :doc:`contributing` guide or check out the project on GitHub.