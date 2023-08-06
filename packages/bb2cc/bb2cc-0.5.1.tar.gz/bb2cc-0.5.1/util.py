"""Utility module with shared functionality."""

import os
import re
import yaml


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
        _, frontmatter, body = re.split(r'\s*---\n\s*', content, 2)
    except ValueError:
        raise IncompatibleDocument(
            file, 'Document frontmatter must be fenced by "---" lines.')

    try:
        frontmatter = yaml.safe_load(frontmatter)
    except yaml.error.YAMLError:
        raise IncompatibleDocument(
            file,
            'Document frontmatter should be valid YAML.')

    if 'page_id' not in frontmatter:
        raise IncompatibleDocument(file, 'The page_id property is required.')

    return frontmatter, body
