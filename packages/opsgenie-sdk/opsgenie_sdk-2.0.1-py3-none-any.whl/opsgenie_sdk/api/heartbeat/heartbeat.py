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


class Heartbeat(object):
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
        'name': 'str',
        'description': 'str',
        'interval': 'int',
        'enabled': 'bool',
        'interval_unit': 'str',
        'expired': 'bool',
        'last_ping_time': 'datetime'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'interval': 'interval',
        'enabled': 'enabled',
        'interval_unit': 'intervalUnit',
        'expired': 'expired',
        'last_ping_time': 'lastPingTime'
    }

    def __init__(self, name=None, description=None, interval=None, enabled=None, interval_unit=None, expired=None, last_ping_time=None):  # noqa: E501
        """Heartbeat - a model defined in OpenAPI"""  # noqa: E501

        self._name = None
        self._description = None
        self._interval = None
        self._enabled = None
        self._interval_unit = None
        self._expired = None
        self._last_ping_time = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if interval is not None:
            self.interval = interval
        if enabled is not None:
            self.enabled = enabled
        if interval_unit is not None:
            self.interval_unit = interval_unit
        if expired is not None:
            self.expired = expired
        if last_ping_time is not None:
            self.last_ping_time = last_ping_time

    @property
    def name(self):
        """Gets the name of this Heartbeat.  # noqa: E501


        :return: The name of this Heartbeat.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Heartbeat.


        :param name: The name of this Heartbeat.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """Gets the description of this Heartbeat.  # noqa: E501


        :return: The description of this Heartbeat.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Heartbeat.


        :param description: The description of this Heartbeat.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def interval(self):
        """Gets the interval of this Heartbeat.  # noqa: E501


        :return: The interval of this Heartbeat.  # noqa: E501
        :rtype: int
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this Heartbeat.


        :param interval: The interval of this Heartbeat.  # noqa: E501
        :type: int
        """

        self._interval = interval

    @property
    def enabled(self):
        """Gets the enabled of this Heartbeat.  # noqa: E501


        :return: The enabled of this Heartbeat.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this Heartbeat.


        :param enabled: The enabled of this Heartbeat.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def interval_unit(self):
        """Gets the interval_unit of this Heartbeat.  # noqa: E501


        :return: The interval_unit of this Heartbeat.  # noqa: E501
        :rtype: str
        """
        return self._interval_unit

    @interval_unit.setter
    def interval_unit(self, interval_unit):
        """Sets the interval_unit of this Heartbeat.


        :param interval_unit: The interval_unit of this Heartbeat.  # noqa: E501
        :type: str
        """
        allowed_values = ["minutes", "hours", "days"]  # noqa: E501
        if interval_unit not in allowed_values:
            raise ValueError(
                "Invalid value for `interval_unit` ({0}), must be one of {1}"  # noqa: E501
                .format(interval_unit, allowed_values)
            )

        self._interval_unit = interval_unit

    @property
    def expired(self):
        """Gets the expired of this Heartbeat.  # noqa: E501


        :return: The expired of this Heartbeat.  # noqa: E501
        :rtype: bool
        """
        return self._expired

    @expired.setter
    def expired(self, expired):
        """Sets the expired of this Heartbeat.


        :param expired: The expired of this Heartbeat.  # noqa: E501
        :type: bool
        """

        self._expired = expired

    @property
    def last_ping_time(self):
        """Gets the last_ping_time of this Heartbeat.  # noqa: E501


        :return: The last_ping_time of this Heartbeat.  # noqa: E501
        :rtype: datetime
        """
        return self._last_ping_time

    @last_ping_time.setter
    def last_ping_time(self, last_ping_time):
        """Sets the last_ping_time of this Heartbeat.


        :param last_ping_time: The last_ping_time of this Heartbeat.  # noqa: E501
        :type: datetime
        """

        self._last_ping_time = last_ping_time

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
        if not isinstance(other, Heartbeat):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
