import base64
import os
from urllib.parse import urljoin

import requests

from gerby.secrets import PIVOTAL_TOKEN


class PivotalTrackerClient(object):
    """Pivotal Tracker client for interactic with their v5 REST API"""

    base_url = "https://www.pivotaltracker.com/services/v5/"
    time_off_id = 16121361

    def __init__(self, token=PIVOTAL_TOKEN):
        """
        Args:
            token (str): pivotal api token
        Returns:
            instance of pivotal client
        """
        self.headers = {
            "accept": "application/json",
            "X-TrackerToken": token,
            "Content-Type": "application/json",
        }

    def _post(self, url, **kwargs):
        response = requests.post(
            urljoin(self.base_url, url), headers=self.headers, params=kwargs
        )
        response.raise_for_status()
        return response.json()

    def _get(self, url, **kwargs):
        response = requests.get(
            urljoin(self.base_url, url), headers=self.headers, params=kwargs
        )
        response.raise_for_status()
        return response.json()

    def project(self, project_id):
        return self._get("projects/" + str(invoice_id))

    def projects(self, **kwargs):
        return self._get("projects", **kwargs)

    def stories(self, project_id, **kwargs):
        return self._get(f"projects/{project_id}/stories", **kwargs)
