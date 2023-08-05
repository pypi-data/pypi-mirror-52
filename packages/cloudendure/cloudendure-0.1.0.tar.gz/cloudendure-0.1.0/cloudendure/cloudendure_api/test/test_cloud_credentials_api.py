# coding: utf-8

"""
    CloudEndure API documentation

    © 2017 CloudEndure All rights reserved  # General Request authentication in CloudEndure's API is done using session cookies. A session cookie is returned upon successful execution of the \"login\" method. This value must then be provided within the request headers of all subsequent API requests.  ## Errors Some errors are not specifically written in every method since they may always return. Those are: 1) 401 (Unauthorized) - for unauthenticated requests. 2) 405 (Method Not Allowed) - for using a method that is not supported (POST instead of GET). 3) 403 (Forbidden) - request is authenticated, but the user is not allowed to access. 4) 422 (Unprocessable Entity) - for invalid input.  ## Formats All strings with date-time format are according to RFC3339.  All strings with \"duration\" format are according to ISO8601. For example, a full day duration can be specified with \"PNNNND\".   # noqa: E501

    OpenAPI spec version: 5
    Contact: https://bit.ly/2T54hSc
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

from api.cloud_credentials_api import CloudCredentialsApi  # noqa: E501
from cloudendure import cloudendure_api
from cloudendure.cloudendure_api.rest import ApiException


class TestCloudCredentialsApi(unittest.TestCase):
    """CloudCredentialsApi unit test stubs"""

    def setUp(self):
        self.api = api.cloud_credentials_api.CloudCredentialsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_cloud_credentials_creds_id_get(self):
        """Test case for cloud_credentials_creds_id_get

        Get Credentials  # noqa: E501
        """
        pass

    def test_cloud_credentials_creds_id_patch(self):
        """Test case for cloud_credentials_creds_id_patch

        Change Credentials  # noqa: E501
        """
        pass

    def test_cloud_credentials_get(self):
        """Test case for cloud_credentials_get

        List Credentials  # noqa: E501
        """
        pass

    def test_cloud_credentials_post(self):
        """Test case for cloud_credentials_post

        Create Credentials  # noqa: E501
        """
        pass


if __name__ == "__main__":
    unittest.main()
