# coding: utf-8

"""
    Python SDK for Opsgenie REST API

    Python SDK for Opsgenie REST API  # noqa: E501

    The version of the OpenAPI document: 2.0.0
    Contact: support@opsgenie.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class AddDetailsToAlertPayloadAllOf(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'details': 'dict(str, str)'
    }

    attribute_map = {
        'details': 'details'
    }

    def __init__(self, details=None):  # noqa: E501
        """AddDetailsToAlertPayloadAllOf - a model defined in OpenAPI"""  # noqa: E501

        self._details = None
        self.discriminator = None

        self.details = details

    @property
    def details(self):
        """Gets the details of this AddDetailsToAlertPayloadAllOf.  # noqa: E501

        Key-value pairs to add as custom property into alert. You can refer here for example values  # noqa: E501

        :return: The details of this AddDetailsToAlertPayloadAllOf.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._details

    @details.setter
    def details(self, details):
        """Sets the details of this AddDetailsToAlertPayloadAllOf.

        Key-value pairs to add as custom property into alert. You can refer here for example values  # noqa: E501

        :param details: The details of this AddDetailsToAlertPayloadAllOf.  # noqa: E501
        :type: dict(str, str)
        """
        if details is None:
            raise ValueError("Invalid value for `details`, must not be `None`")  # noqa: E501

        self._details = details

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, AddDetailsToAlertPayloadAllOf):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
