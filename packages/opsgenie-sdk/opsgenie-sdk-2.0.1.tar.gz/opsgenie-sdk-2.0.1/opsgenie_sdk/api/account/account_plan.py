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


class AccountPlan(object):
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
        'max_user_count': 'int',
        'name': 'str',
        'is_yearly': 'bool'
    }

    attribute_map = {
        'max_user_count': 'maxUserCount',
        'name': 'name',
        'is_yearly': 'isYearly'
    }

    def __init__(self, max_user_count=None, name=None, is_yearly=None):  # noqa: E501
        """AccountPlan - a model defined in OpenAPI"""  # noqa: E501

        self._max_user_count = None
        self._name = None
        self._is_yearly = None
        self.discriminator = None

        if max_user_count is not None:
            self.max_user_count = max_user_count
        if name is not None:
            self.name = name
        if is_yearly is not None:
            self.is_yearly = is_yearly

    @property
    def max_user_count(self):
        """Gets the max_user_count of this AccountPlan.  # noqa: E501


        :return: The max_user_count of this AccountPlan.  # noqa: E501
        :rtype: int
        """
        return self._max_user_count

    @max_user_count.setter
    def max_user_count(self, max_user_count):
        """Sets the max_user_count of this AccountPlan.


        :param max_user_count: The max_user_count of this AccountPlan.  # noqa: E501
        :type: int
        """

        self._max_user_count = max_user_count

    @property
    def name(self):
        """Gets the name of this AccountPlan.  # noqa: E501


        :return: The name of this AccountPlan.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AccountPlan.


        :param name: The name of this AccountPlan.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def is_yearly(self):
        """Gets the is_yearly of this AccountPlan.  # noqa: E501


        :return: The is_yearly of this AccountPlan.  # noqa: E501
        :rtype: bool
        """
        return self._is_yearly

    @is_yearly.setter
    def is_yearly(self, is_yearly):
        """Sets the is_yearly of this AccountPlan.


        :param is_yearly: The is_yearly of this AccountPlan.  # noqa: E501
        :type: bool
        """

        self._is_yearly = is_yearly

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
        if not isinstance(other, AccountPlan):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
