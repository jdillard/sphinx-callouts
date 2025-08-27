import re
from docutils import nodes

from sphinx.util.docutils import SphinxDirective
from sphinx.transforms import SphinxTransform
from docutils.nodes import Node

__version__ = "0.1.0"

# BASE_NUM = 2775  # black circles, white numbers
BASE_NUM = 2459  # white circle, black numbers


class CalloutIncludePostTransform(SphinxTransform):
    """Code block post-processor for `literalinclude` blocks used in callouts."""

    default_priority = 400

    def apply(self, **kwargs) -> None:
        visitor = LiteralIncludeVisitor(self.document)
        self.document.walkabout(visitor)


class LiteralIncludeVisitor(nodes.NodeVisitor):
    """Change a literal block upon visiting it."""

    def __init__(self, document: nodes.document) -> None:
        super().__init__(document)

    def _is_inside_callout(self, node: nodes.literal_block) -> bool:
        """Check if the literal block is inside a callout directive."""
        parent = node.parent
        while parent is not None:
            if isinstance(parent, callout):
                return True
            parent = parent.parent
        return False

    def unknown_visit(self, node: Node) -> None:
        pass

    def unknown_departure(self, node: Node) -> None:
        pass

    def visit_document(self, node: Node) -> None:
        pass

    def depart_document(self, node: Node) -> None:
        pass

    def visit_start_of_file(self, node: Node) -> None:
        pass

    def depart_start_of_file(self, node: Node) -> None:
        pass

    def visit_literal_block(self, node: nodes.literal_block) -> None:
        # Only process literal blocks that are inside a callout node
        if self._is_inside_callout(node):
            # Get source content - try rawsource first, then text content
            source = ""
            if hasattr(node, 'rawsource') and node.rawsource:
                source = str(node.rawsource)
            elif len(node.children) > 0 and hasattr(node.children[0], 'rawsource'):
                source = str(node.children[0].rawsource)
            elif len(node.children) > 0:
                source = str(node.children[0])
            else:
                source = str(node.astext())

            # Only process if we found callout markers
            if "<1>" not in source:
                return
            callouts = []
            lines = source.split('\n')
            clean_lines = []

            # Process each line to extract callouts and clean the code
            for line_num, line in enumerate(lines):
                clean_line = line
                # Find all callout markers in this line
                for i in range(1, 20):
                    marker = f"<{i}>"
                    if marker in line:
                        # Record the callout position and number
                        callouts.append({
                            'line': line_num,
                            'number': i,
                            'symbol': chr(int(f"0x{BASE_NUM + i}", base=16))
                        })
                        # Remove the comment and marker from the line
                        # Supports different comment patterns with regex for whitespace-agnostic matching
                        # Escape marker for regex (handles < > characters in markers like <7>)
                        escaped_marker = re.escape(marker)
                        escaped_number = re.escape(str(i))
                        # Define regex patterns (ordered by specificity - most specific first)
                        regex_patterns = [
                            # XML/HTML/SGML style comments with flexible whitespace
                            rf'\s*<!--\s*{escaped_marker}\s*-->\s*',      # <!--<7>--> with optional spaces
                            rf'\s*<!--\s*{escaped_number}\s*-->\s*',      # <!--7--> with optional spaces

                            # Python/Ruby/Perl/Shell style comments
                            rf'\s*#\s*{escaped_marker}\s*',               # # <7> with flexible spacing

                            # C-style comments (C++, Java, JavaScript, etc.)
                            rf'\s*//\s*{escaped_marker}\s*',              # // <7> with flexible spacing

                            # Clojure style comments
                            rf'\s*;;\s*{escaped_marker}\s*',              # ;; <7> with flexible spacing

                            # Erlang/PostScript style comments
                            rf'\s*%\s*{escaped_marker}\s*',               # % <7> with flexible spacing

                            # SQL style comments
                            rf'\s*--\s*{escaped_marker}\s*',              # -- <7> with flexible spacing

                            # Fortran/MATLAB style comments
                            rf'\s*!\s*{escaped_marker}\s*',               # ! <7> with flexible spacing

                            # Fallback: just the marker with optional surrounding whitespace
                            rf'\s*{escaped_marker}\s*'                    # <7> with optional spacing
                        ]

                        # Try each regex pattern until one matches
                        pattern_matched = False
                        for regex_pattern in regex_patterns:
                            if re.search(regex_pattern, clean_line):
                                clean_line = re.sub(regex_pattern, '', clean_line, count=1)
                                pattern_matched = True
                                break


                # Clean up any remaining whitespace where markers were removed
                clean_line = clean_line.rstrip()
                clean_lines.append(clean_line)

            # Set the clean source without markers
            clean_source = '\n'.join(clean_lines)

            if callouts:
                # Create a new callout_literal_block node to replace this one
                callout_node = callout_literal_block(clean_source, **node.attributes)
                callout_node['callouts'] = callouts
                callout_node['language'] = node.get('language', '')

                # Replace the current node with our custom node
                node.parent.replace(node, callout_node)
            else:
                # No callouts found, keep original behavior
                node.rawsource = clean_source
                node[:] = [nodes.Text(clean_source)]


class callout_literal_block(nodes.literal_block):
    """Custom literal block node that contains callout information."""
    pass


class callout(nodes.General, nodes.Element):
    """Sphinx callout node."""

    pass


def visit_callout_node(self, node):
    """Add callout CSS class to the wrapper div."""
    self.body.append('<div class="callout">')


def depart_callout_node(self, node):
    """Close the callout wrapper div."""
    self.body.append('</div>')


def visit_callout_literal_block_html(self, node):
    """Custom HTML rendering for literal blocks with callouts."""
    callouts = node.get('callouts', [])
    callouts_by_line = {c['line']: c for c in callouts}

    # Start the wrapper div
    self.body.append('<div class="callout-code-wrapper">')

    # Render the code block with inline callouts
    attrs = node.non_default_attributes()
    classes = ['highlight']
    if node.get('language'):
        classes.append(f'highlight-{node.get("language")}')
    attrs['class'] = ' '.join(classes)

    # Build the div tag
    tag_attrs = ''.join(f' {k}="{v}"' for k, v in attrs.items())
    self.body.append(f'<div{tag_attrs}>')
    self.body.append('<div class="highlight">')
    self.body.append('<pre>')

    # Process content line by line to insert inline callouts
    content = str(node.rawsource) if hasattr(node, 'rawsource') else str(node)
    lines = content.split('\n')

    for line_num, line in enumerate(lines):
        # Escape HTML special characters
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        # Add the line content
        self.body.append(escaped_line)

        # Add inline callout if this line has one
        if line_num in callouts_by_line:
            callout = callouts_by_line[line_num]
            self.body.append(f'<span class="callout-inline-marker"> {callout["symbol"]}</span>')

        # Add newline except for the last line
        if line_num < len(lines) - 1:
            self.body.append('\n')


def depart_callout_literal_block_html(self, node):
    """Custom HTML rendering for literal blocks with callouts."""
    # Close the pre and highlight divs
    self.body.append('</pre>')
    self.body.append('</div>')
    self.body.append('</div>')

    # Close the wrapper div
    self.body.append('</div>')


class annotations(nodes.Element):
    """Sphinx annotations node."""

    pass


def visit_annotations_node(self, node):
    """Add annotations CSS class to the wrapper div."""
    self.body.append('<div class="annotations">')


def depart_annotations_node(self, node):
    """Close the annotations wrapper div."""
    self.body.append('</div>')


def _replace_numbers(content):
    """
    Replaces strings of the form <x> with circled unicode numbers (e.g. ①) as text.

    Args:
        content: List of strings or string from a callout or annotations directive.

    Returns: The formatted content.
    """
    if isinstance(content, list):
        result = []
        for line in content:
            if line is not None:
                for i in range(1, 20):
                    line = line.replace(f"<{i}>", chr(int(f"0x{BASE_NUM + i}", base=16)))
                result.append(line)
            else:
                result.append(line)
        return result
    elif isinstance(content, str):
        for i in range(1, 20):
            content = content.replace(f"<{i}>", chr(int(f"0x{BASE_NUM + i}", base=16)))
        return content
    else:
        return content


def _parse_recursively(self, node):
    """Utility to recursively parse a node from the Sphinx AST."""
    self.state.nested_parse(self.content, self.content_offset, node)


class CalloutDirective(SphinxDirective):
    """Code callout directive with annotations for Sphinx.

    Use this `callout` directive by wrapping either `code-block` or `literalinclude`
    directives. Each line that's supposed to be equipped with an annotation should
    have an inline comment of the form "# <x>" where x is an integer.

    Afterwards use the `annotations` directive to add annotations to the previously
    defined code labels ("<x>") by using the syntax "<x> my annotation" to produce an
    annotation "my annotation" for x.
    Note that annotation lines have to be separated by a new line, i.e.

    .. annotations::

        <1> First comment followed by a newline,

        <2> second comment after the newline.


    Usage example:
    -------------

    .. callout::

        .. code-block:: python

            from ray import tune
            from ray.tune.search.hyperopt import HyperOptSearch
            import keras

            def objective(config):  # <1>
                ...

            search_space = {"activation": tune.choice(["relu", "tanh"])}  # <2>
            algo = HyperOptSearch()

            tuner = tune.Tuner(  # <3>
                ...
            )
            results = tuner.fit()

        .. annotations::

            <1> Wrap a Keras model in an objective function.

            <2> Define a search space and initialize the search algorithm.

            <3> Start a Tune run that maximizes accuracy.
    """

    has_content = True

    def run(self):
        self.assert_has_content()

        content = self.content

        callout_node = callout("\n".join(content))
        _parse_recursively(self, callout_node)

        return [callout_node]


class AnnotationsDirective(SphinxDirective):
    """Annotations directive, which is only used nested within a Callout directive."""

    has_content = True

    def run(self):
        content = self.content
        content = _replace_numbers(content)

        joined_content = "\n".join(content)
        annotations_node = annotations(joined_content)
        _parse_recursively(self, annotations_node)

        return [annotations_node]


def setup(app):
    import os.path

    # Add static files path
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '_static'))
    app.config.html_static_path.append(static_path)

    # Add new node types
    app.add_node(
        callout,
        html=(visit_callout_node, depart_callout_node),
        latex=(visit_callout_node, depart_callout_node),
        text=(visit_callout_node, depart_callout_node),
    )
    app.add_node(
        callout_literal_block,
        html=(visit_callout_literal_block_html, depart_callout_literal_block_html),
        latex=(visit_callout_node, depart_callout_node),
        text=(visit_callout_node, depart_callout_node),
    )
    app.add_node(
        annotations,
        html=(visit_annotations_node, depart_annotations_node),
        latex=(visit_callout_node, depart_callout_node),
        text=(visit_callout_node, depart_callout_node),
    )

    # Add new directives
    app.add_directive("callout", CalloutDirective)
    app.add_directive("annotations", AnnotationsDirective)

    # Add post-processor
    app.add_post_transform(CalloutIncludePostTransform)

    # Add CSS for callouts
    app.add_css_file('css/callouts.css')

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
