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


class AddTeamToAlertPayload(object):
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
        'user': 'str',
        'note': 'str',
        'source': 'str',
        'team': 'TeamRecipient'
    }

    attribute_map = {
        'user': 'user',
        'note': 'note',
        'source': 'source',
        'team': 'team'
    }

    def __init__(self, user=None, note=None, source=None, team=None):  # noqa: E501
        """AddTeamToAlertPayload - a model defined in OpenAPI"""  # noqa: E501

        self._user = None
        self._note = None
        self._source = None
        self._team = None
        self.discriminator = None

        if user is not None:
            self.user = user
        if note is not None:
            self.note = note
        if source is not None:
            self.source = source
        self.team = team

    @property
    def user(self):
        """Gets the user of this AddTeamToAlertPayload.  # noqa: E501

        Display name of the request owner  # noqa: E501

        :return: The user of this AddTeamToAlertPayload.  # noqa: E501
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, user):
        """Sets the user of this AddTeamToAlertPayload.

        Display name of the request owner  # noqa: E501

        :param user: The user of this AddTeamToAlertPayload.  # noqa: E501
        :type: str
        """

        self._user = user

    @property
    def note(self):
        """Gets the note of this AddTeamToAlertPayload.  # noqa: E501

        Additional note that will be added while creating the alert  # noqa: E501

        :return: The note of this AddTeamToAlertPayload.  # noqa: E501
        :rtype: str
        """
        return self._note

    @note.setter
    def note(self, note):
        """Sets the note of this AddTeamToAlertPayload.

        Additional note that will be added while creating the alert  # noqa: E501

        :param note: The note of this AddTeamToAlertPayload.  # noqa: E501
        :type: str
        """

        self._note = note

    @property
    def source(self):
        """Gets the source of this AddTeamToAlertPayload.  # noqa: E501

        Source field of the alert. Default value is IP address of the incoming request  # noqa: E501

        :return: The source of this AddTeamToAlertPayload.  # noqa: E501
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """Sets the source of this AddTeamToAlertPayload.

        Source field of the alert. Default value is IP address of the incoming request  # noqa: E501

        :param source: The source of this AddTeamToAlertPayload.  # noqa: E501
        :type: str
        """

        self._source = source

    @property
    def team(self):
        """Gets the team of this AddTeamToAlertPayload.  # noqa: E501


        :return: The team of this AddTeamToAlertPayload.  # noqa: E501
        :rtype: TeamRecipient
        """
        return self._team

    @team.setter
    def team(self, team):
        """Sets the team of this AddTeamToAlertPayload.


        :param team: The team of this AddTeamToAlertPayload.  # noqa: E501
        :type: TeamRecipient
        """
        if team is None:
            raise ValueError("Invalid value for `team`, must not be `None`")  # noqa: E501

        self._team = team

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
        if not isinstance(other, AddTeamToAlertPayload):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
