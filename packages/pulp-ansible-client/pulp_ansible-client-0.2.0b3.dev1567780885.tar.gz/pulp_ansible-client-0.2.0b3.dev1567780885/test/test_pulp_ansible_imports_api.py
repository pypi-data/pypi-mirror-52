# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulp_ansible
from pulpcore.client.pulp_ansible.api.pulp_ansible_imports_api import PulpAnsibleImportsApi  # noqa: E501
from pulpcore.client.pulp_ansible.rest import ApiException


class TestPulpAnsibleImportsApi(unittest.TestCase):
    """PulpAnsibleImportsApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulp_ansible.api.pulp_ansible_imports_api.PulpAnsibleImportsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_list(self):
        """Test case for list

        List collection imports  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
