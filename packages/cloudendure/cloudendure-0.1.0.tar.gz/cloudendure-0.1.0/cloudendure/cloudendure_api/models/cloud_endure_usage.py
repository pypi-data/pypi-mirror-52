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


class CloudEndureUsage:
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
        "start_of_use_date_time": "datetime",
        "cloud_id": "str",
        "name": "str",
        "machine_id": "str",
    }

    attribute_map = {
        "start_of_use_date_time": "startOfUseDateTime",
        "cloud_id": "cloudId",
        "name": "name",
        "machine_id": "machineId",
    }

    def __init__(
        self, start_of_use_date_time=None, cloud_id=None, name=None, machine_id=None
    ):  # noqa: E501
        """CloudEndureUsage - a model defined in Swagger"""  # noqa: E501
        self._start_of_use_date_time = None
        self._cloud_id = None
        self._name = None
        self._machine_id = None
        self.discriminator = None
        if start_of_use_date_time is not None:
            self.start_of_use_date_time = start_of_use_date_time
        if cloud_id is not None:
            self.cloud_id = cloud_id
        if name is not None:
            self.name = name
        if machine_id is not None:
            self.machine_id = machine_id

    @property
    def start_of_use_date_time(self):
        """Gets the start_of_use_date_time of this CloudEndureUsage.  # noqa: E501


        :return: The start_of_use_date_time of this CloudEndureUsage.  # noqa: E501
        :rtype: datetime
        """
        return self._start_of_use_date_time

    @start_of_use_date_time.setter
    def start_of_use_date_time(self, start_of_use_date_time):
        """Sets the start_of_use_date_time of this CloudEndureUsage.


        :param start_of_use_date_time: The start_of_use_date_time of this CloudEndureUsage.  # noqa: E501
        :type: datetime
        """

        self._start_of_use_date_time = start_of_use_date_time

    @property
    def cloud_id(self):
        """Gets the cloud_id of this CloudEndureUsage.  # noqa: E501

        The ID in the cloud  # noqa: E501

        :return: The cloud_id of this CloudEndureUsage.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this CloudEndureUsage.

        The ID in the cloud  # noqa: E501

        :param cloud_id: The cloud_id of this CloudEndureUsage.  # noqa: E501
        :type: str
        """

        self._cloud_id = cloud_id

    @property
    def name(self):
        """Gets the name of this CloudEndureUsage.  # noqa: E501

        The name of the machine.  # noqa: E501

        :return: The name of this CloudEndureUsage.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CloudEndureUsage.

        The name of the machine.  # noqa: E501

        :param name: The name of this CloudEndureUsage.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def machine_id(self):
        """Gets the machine_id of this CloudEndureUsage.  # noqa: E501


        :return: The machine_id of this CloudEndureUsage.  # noqa: E501
        :rtype: str
        """
        return self._machine_id

    @machine_id.setter
    def machine_id(self, machine_id):
        """Sets the machine_id of this CloudEndureUsage.


        :param machine_id: The machine_id of this CloudEndureUsage.  # noqa: E501
        :type: str
        """

        self._machine_id = machine_id

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
        if issubclass(CloudEndureUsage, dict):
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
        if not isinstance(other, CloudEndureUsage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
