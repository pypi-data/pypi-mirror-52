#!/usr/bin/python
# -*- coding: utf-8 -*-

from monkey.google.api.helpers import GSuiteService, CredentialProvider, GoogleAPIError
from googleapiclient.errors import HttpError


class GroupSettingsService(GSuiteService):

    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('groupssettings', 'v1', credential_provider)

    def get_settings(self, group_id):
        settings = self.service.groups().get(groupUniqueId=group_id).execute()
        return settings

    def update_settings(self, group_id, new_settings):
        settings = self.service.groups().update(groupUniqueId=group_id, body=new_settings).execute()
        return settings
