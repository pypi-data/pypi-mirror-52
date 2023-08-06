"""Convert a Markdown document to Confluence-compatible HTML."""

import re

import mistune


class ConfluenceRenderer(mistune.Renderer):
    """Class that renders HTML that can be uploaded to a Confluence page."""

    def block_code(self, code, language=None):
        """Render a block of source code.

        This method introduces a special case for the code block syntax where
        the "language" is set to `panel:<type>`.
        """
        panel_match = re.match(r'^panel:(info|warning|success|error)$',
                               language or '')

        if not panel_match:
            return super().block_code(code, language)

        def map_panel_type(panel_type):
            # The type strings that Confluence uses for its panels are not
            # very intuitive!
            if panel_type == 'info':
                return 'info'
            elif panel_type == 'warning':
                return 'note'
            elif panel_type == 'success':
                return 'tip'
            elif panel_type == 'error':
                return 'warning'
            raise ValueError('Invalid panel type: {}'.format(panel_type))

        return self.info_panel(map_panel_type(panel_match.group(1)),
                               render_to_html(code))

    def text(self, text):
        """Strip non-semantic whitespace from a text node."""
        return re.sub(r'\s+', ' ', text)

    def status_lozenge(self, color, label):
        """Render a status lozenge with the given color and label."""
        return (
            '<ac:structured-macro ac:name="status">'
            '<ac:parameter ac:name="colour">{color}</ac:parameter>'
            '<ac:parameter ac:name="title">{label}</ac:parameter>'
            '</ac:structured-macro>'
        ).format(color=color, label=label)

    def info_panel(self, style, body):
        """Render a panel with the given style (e.g. info) and body."""
        return (
            '<ac:structured-macro ac:name="{style}">'
            '<ac:rich-text-body>{body}</ac:rich-text-body>'
            '</ac:structured-macro>'
        ).format(style=style, body=body)


class ConfluenceLexer(mistune.InlineLexer):
    """Class that parses custom syntax for various Confluence macros."""

    def __init__(self, *args, **kwargs):
        """Initialize and enable new grammar rules."""
        super().__init__(*args, **kwargs)
        self.enable_status_lozenge()

    def add_default_rule(self, rule_name):
        """Add a new default syntax rule."""
        text_index = self.default_rules.index('text')

        # Insert *before* text (which catches everything).
        self.default_rules.insert(text_index, rule_name)

    def enable_status_lozenge(self):
        """Enable a new `[[Label|Color]]` syntax for status lozenges."""
        self.rules.status_lozenge = re.compile(
            r'\[\['                  # [[
            r'([^:]+(?::[^:\]]+)?)'  # "Label:Color" or just "Label"
            r'\]\](?!\])'            # ]]
        )

        self.add_default_rule('status_lozenge')

    def output_status_lozenge(self, match):
        """Render a status lozenge for the given re.Match object."""
        text = match.group(1)
        if ':' in text:
            title, color = text.split(':')
        else:
            title = text
            color = 'Grey'

        return self.renderer.status_lozenge(color, title)


def render_to_html(text):
    """Render some Markdown text to Confluence-compatible HTML."""
    renderer = ConfluenceRenderer()
    lexer = ConfluenceLexer(renderer)
    markdown = mistune.Markdown(renderer=renderer, inline=lexer)
    return markdown(text)
