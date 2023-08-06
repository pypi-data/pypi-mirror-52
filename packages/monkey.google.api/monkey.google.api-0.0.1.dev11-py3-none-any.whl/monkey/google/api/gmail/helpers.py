#!/usr/bin/python
# -*- coding: utf-8 -*-

from monkey.google.api.helpers import GSuiteService, CredentialProvider, GoogleAPIError
from googleapiclient.errors import HttpError


class GmailService(GSuiteService):
    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('gmail', 'v1', credential_provider)

    def list_labels(self, user_id='me'):
        results = self.service.users().labels().list(userId=user_id).execute()
        labels = results.get('labels', [])
        return labels

    def get_label(self, label_id, user_id='me'):
        label = self.service.users().labels().get(id=label_id, userId=user_id).execute()
        return label

    def create_label(self, name, user_id='me', label_list_visibility='labelShow', message_list_visibility='show'):
        label_def = {
            'name': name,
            'labelListVisibility': label_list_visibility,
            'messageListVisibility' : message_list_visibility
        }
        try:
            label = self.service.users().labels().create(userId=user_id, body=label_def).execute()
            return label
        except HttpError as e:
            raise GoogleAPIError('Unexpected error.', e)
