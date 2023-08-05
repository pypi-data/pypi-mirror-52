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


class CloseIncidentPayload(object):
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
        'note': 'str'
    }

    attribute_map = {
        'note': 'note'
    }

    def __init__(self, note=None):  # noqa: E501
        """CloseIncidentPayload - a model defined in OpenAPI"""  # noqa: E501

        self._note = None
        self.discriminator = None

        if note is not None:
            self.note = note

    @property
    def note(self):
        """Gets the note of this CloseIncidentPayload.  # noqa: E501

        Additional note that will be included with the incident  # noqa: E501

        :return: The note of this CloseIncidentPayload.  # noqa: E501
        :rtype: str
        """
        return self._note

    @note.setter
    def note(self, note):
        """Sets the note of this CloseIncidentPayload.

        Additional note that will be included with the incident  # noqa: E501

        :param note: The note of this CloseIncidentPayload.  # noqa: E501
        :type: str
        """

        self._note = note

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
        if not isinstance(other, CloseIncidentPayload):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
