#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os.path
import pickle

import googleapiclient.discovery
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client.service_account import ServiceAccountCredentials


class CredentialProvider(object):
    def __init__(self, scopes):
        self.logger = logging.getLogger('monkey.google.api.helpers.CredentialProvider')
        self.scopes = scopes
        self.credentials = None

    def authorize(self, http):
        return self.credentials.authorize(http)


class UserCredentialProvider(CredentialProvider):

    def __init__(self, scopes, credential_file, token_file):
        super().__init__(scopes)
        credentials = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)
                self.logger.debug('Existing token loaded.')
        # If there are no (valid) credentials available, let the user log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                self.logger.debug('Expired credentials, refreshing with refresh token.')
                credentials.refresh(Request())
            else:
                self.logger.debug('Expired credentials without refresh token.')
                flow = InstalledAppFlow.from_client_secrets_file(credential_file, scopes)
                credentials = flow.run_local_server()
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
                self.logger.debug('New token successfully saved.')
        self.credentials = credentials


class ServiceAccountCredentialProvider(CredentialProvider):

    def __init__(self, scopes, credential_file, impersonate_user_email):
        super().__init__(scopes)
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_file, scopes)
        self.credentials = credentials.create_delegated(impersonate_user_email)


class GoogleAPIError(Exception):

    def __init__(self, message='Google API error', cause=None):
        self.message = message
        self.cause = cause


class GSuiteService:

    def __init__(self, name, version, credential_provider: CredentialProvider):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = name
        self.version = version
        self.credential_provider = credential_provider

        # WORKAROUND: Disable cache to avoid ImportError due to oauthclien >= 4.0.0
        # SEE: https://stackoverflow.com/questions/40154672/importerror-file-cache-is-unavailable-when-using-python-client-for-google-ser)
        self.service = googleapiclient.discovery.build(self.name, self.version,
                                                       credentials=self.credential_provider.credentials,
                                                       cache_discovery=False)

    def list_all(self):
        raise NotImplemented()


class PeopleService(GSuiteService):

    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('people', 'v1', credential_provider)

    def list_all(self):
        raise NotImplementedError()


class SheetService(GSuiteService):

    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('sheets', 'v4', credential_provider)
