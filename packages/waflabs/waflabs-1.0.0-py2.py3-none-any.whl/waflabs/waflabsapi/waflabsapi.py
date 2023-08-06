"""
WAFLABS API Client
"""

import requests
import waflabs

class WAFLabsApi(object):
    """
    Class for WAFLABS API
    """
    base_url = "https://waflabs.com/api/"
    api_version = "v0"
    access_id = ""
    api_secret = ""

    def __init__(self, access_id, access_key):
        """
        Init waflabsapi
        """
        self.access_id = access_id
        self.access_key = access_key

    def _make_request(self,
                      endpoint,
                      params=None,
                      json=None,
                      method="GET"):

        headers = dict()
        headers["x-access-id"] = self.access_id
        headers['x-access-key'] = self.access_key
        headers["Content-Type"] = "application/json"
        headers['User-Agent'] = 'waflabs v' + waflabs.VERSION

        url = self.base_url + self.api_version + endpoint

        result = None
        if method == "GET":
            del headers["Content-Type"]
            result = requests.get(url, params=params, headers=headers)
        elif method == "POST":
            result = requests.post(url, json=json, headers=headers)
        else:
            raise Exception("InvalidRequestMethod: " + str(method))

        if result.status_code == 204:
            return dict({'message': '{} {}'.format(method, 'successful.')})

        if result.status_code == 400:
            raise Exception('400 Bad Request')

        return result.json()

    def testmywaf(self, payload):
        """
        Test my WAF!
        """
        return self._make_request("/testmywaf", json=payload, method="POST")

    def results(self, run_id):
        """
        Retreive test results
        """
        params = dict()
        params["run_id"] = run_id
        return self._make_request("/results", params=params, method="GET")
    
    def history(self):
        """
        Retreive user test history
        """
        return self._make_request("/results/history", method="GET")
    
    def company_history(self):
        """
        Retreive company test history
        """
        return self._make_request("/results/history/company", method="GET")

    def domain(self, payload):
        """
        Create a domain ownership record, returns ownership validation token
        """
        return self._make_request("/domain", json=payload, method="POST")

    def domain_list(self):
        """
        Returns list of domain ownership records
        """
        return self._make_request("/domain/list", method="GET")

    def domain_validate(self, payload):
        """
        Validate ownership of a domain
        """
        return self._make_request("/domain/validate", json=payload, method="POST")
