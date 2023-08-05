# coding: utf-8

"""
    CloudEndure API documentation

    © 2017 CloudEndure All rights reserved  # General Request authentication in CloudEndure's API is done using session cookies. A session cookie is returned upon successful execution of the \"login\" method. This value must then be provided within the request headers of all subsequent API requests.  ## Errors Some errors are not specifically written in every method since they may always return. Those are: 1) 401 (Unauthorized) - for unauthenticated requests. 2) 405 (Method Not Allowed) - for using a method that is not supported (POST instead of GET). 3) 403 (Forbidden) - request is authenticated, but the user is not allowed to access. 4) 422 (Unprocessable Entity) - for invalid input.  ## Formats All strings with date-time format are according to RFC3339.  All strings with \"duration\" format are according to ISO8601. For example, a full day duration can be specified with \"PNNNND\".   # noqa: E501

    OpenAPI spec version: 5
    Contact: https://bit.ly/2T54hSc
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class CloudEndureComputeLocation:
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "is_encryption_supported": "bool",
        "location_id": "str",
        "name": "str",
    }

    attribute_map = {
        "is_encryption_supported": "isEncryptionSupported",
        "location_id": "locationId",
        "name": "name",
    }

    def __init__(
        self, is_encryption_supported=None, location_id=None, name=None
    ):  # noqa: E501
        """CloudEndureComputeLocation - a model defined in Swagger"""  # noqa: E501
        self._is_encryption_supported = None
        self._location_id = None
        self._name = None
        self.discriminator = None
        if is_encryption_supported is not None:
            self.is_encryption_supported = is_encryption_supported
        if location_id is not None:
            self.location_id = location_id
        if name is not None:
            self.name = name

    @property
    def is_encryption_supported(self):
        """Gets the is_encryption_supported of this CloudEndureComputeLocation.  # noqa: E501


        :return: The is_encryption_supported of this CloudEndureComputeLocation.  # noqa: E501
        :rtype: bool
        """
        return self._is_encryption_supported

    @is_encryption_supported.setter
    def is_encryption_supported(self, is_encryption_supported):
        """Sets the is_encryption_supported of this CloudEndureComputeLocation.


        :param is_encryption_supported: The is_encryption_supported of this CloudEndureComputeLocation.  # noqa: E501
        :type: bool
        """

        self._is_encryption_supported = is_encryption_supported

    @property
    def location_id(self):
        """Gets the location_id of this CloudEndureComputeLocation.  # noqa: E501


        :return: The location_id of this CloudEndureComputeLocation.  # noqa: E501
        :rtype: str
        """
        return self._location_id

    @location_id.setter
    def location_id(self, location_id):
        """Sets the location_id of this CloudEndureComputeLocation.


        :param location_id: The location_id of this CloudEndureComputeLocation.  # noqa: E501
        :type: str
        """

        self._location_id = location_id

    @property
    def name(self):
        """Gets the name of this CloudEndureComputeLocation.  # noqa: E501


        :return: The name of this CloudEndureComputeLocation.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CloudEndureComputeLocation.


        :param name: The name of this CloudEndureComputeLocation.  # noqa: E501
        :type: str
        """

        self._name = name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(CloudEndureComputeLocation, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CloudEndureComputeLocation):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
