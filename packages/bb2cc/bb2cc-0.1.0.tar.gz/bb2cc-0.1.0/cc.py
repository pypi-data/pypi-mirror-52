"""Basic Confluence Cloud API client library."""

import json

from urllib.parse import urljoin

import requests


class Confluence(object):
    """Client for interacting with the Confluence Cloud API."""

    def __init__(self, host, username, password):
        """Initialize a client object for the given host and credentials."""
        self.host = host
        self.session = requests.Session()
        self.session.auth = (username, password)

    def update_page(self, page_id, title=None, content=None):
        """Update a Confluence page with the given title and HTML content.

        This will always override the current version.
        """
        payload = {
            'type': 'page',
            'version': {
                'number': self.get_current_version(page_id) + 1
            }
        }

        if title is not None:
            payload['title'] = title

        if content is not None:
            payload['body'] = {
                'storage': {
                    'value': content,
                    'representation': 'storage'
                }
            }

        url = urljoin(self.host, 'rest/api/content/%(page_id)s') % {
            'page_id': page_id
        }
        response = self.session.put(
            url, headers={'Content-Type': 'application/json'},
            data=json.dumps(payload))
        self.raise_for_status(response)

        response_data = response.json()

        return response_data

    def get_current_version(self, page_id):
        """Get the current version of a Confluence page."""
        url = urljoin(self.host, 'rest/api/content/%(page_id)s') % {
            'page_id': page_id
        }
        response = self.session.get(url)
        self.raise_for_status(response)

        response_data = response.json()

        return response_data['version']['number']

    def raise_for_status(self, response):
        """For non-2xx responses, print the body and raise an exception."""
        if not 200 <= response.status_code < 300:
            print('{}: {}'.format(response.status_code, response.content))
            response.raise_for_status()
