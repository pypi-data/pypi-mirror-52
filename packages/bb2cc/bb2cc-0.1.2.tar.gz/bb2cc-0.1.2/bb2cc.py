"""Sync a Markdown document from a Bitbucket repo to a Confluence page."""

import os
import re

import mistune


class StripNewlineRenderer(mistune.Renderer):
    """Class that strips non-semantic whitespace from HTML."""

    def text(self, text):
        """Remove newline characters from a text node."""
        return re.sub(r'\n', ' ', text)


class IncompatibleDocument(ValueError):
    """Exception raised when a document is not in a compatible format."""

    def __init__(self, file, message):
        """Initialize an error for the given file with a specified message."""
        super().__init__(
            '{} is not in the right format: {}'.format(os.path.basename(file),
                                                       message))


def parse_file(file):
    """Parse the frontmatter and body of a file in Markdown format."""
    with open(file, 'r') as f:
        content = f.read()

    try:
        _, frontmatter, body = re.split(r'\s*---\n\s*', content)
    except ValueError:
        raise IncompatibleDocument(
            file, 'Document frontmatter must be fenced by "---" lines.')

    try:
        frontmatter = {
            key: value
            for key, value in (re.split(r':\s*', pair)
                               for pair in frontmatter.split('\n'))}
    except ValueError:
        raise IncompatibleDocument(
            file,
            'Document frontmatter should consist of <key>: <value> lines.')

    if 'page_id' not in frontmatter:
        raise IncompatibleDocument(file, 'The page_id property is required.')

    return {
        'frontmatter': frontmatter,
        'html': render_to_html(body)
    }


def render_to_html(text):
    """Render some Markdown text to HTML."""
    markdown = mistune.Markdown(renderer=StripNewlineRenderer())
    return markdown(text)


def header_info(repository_url=None):
    """Provide the HTML for an info header to appear at the top of a page.

    If the repository_url argument is provided, the header informs the reader
    that the page is kept in sync with a Bitbucket repository. Otherwise, it
    indicates only that the page was created using bb2cc.
    """
    # It's important for this HTML to have no unnecessary newline characters as
    # these are interpreted as meaningful by the Confluence API and end up
    # getting rendered as extra space on the page.
    opening_tags = '<ac:structured-macro ac:name="info"><ac:rich-text-body>'
    closing_tags = '</ac:rich-text-body></ac:structured-macro>'

    if repository_url:
        paragraphs = (
            '<p>This page is kept in sync with '
            '<a href="{repository_url}">{repository_url}</a> using the '
            '<a href="https://bitbucket.org/dtao/bb2cc">bb2cc</a> '
            'library.</p>'
            '<p>Any changes you make to this page in Confluence will be '
            'overridden on the next push to the repository.</p>'
        ).format(repository_url=repository_url)
    else:
        paragraphs = (
            '<p>This page was created automatically from a Markdown file '
            'using the <a href="https://bitbucket.org/dtao/bb2cc">bb2cc</a> '
            'library.</p>')

    return '{}{}{}'.format(opening_tags, paragraphs, closing_tags)


def sync_to_confluence(client, file, repository_url=None):
    """Sync the given file to an existing Confluence page using the API."""
    data = parse_file(file)
    client.update_page(data['frontmatter']['page_id'],
                       title=data['frontmatter']['title'],
                       content=header_info(repository_url) + data['html'])
