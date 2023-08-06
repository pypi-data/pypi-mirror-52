#!/usr/bin/python
# -*- coding: utf-8 -*-

from monkey.google.api.helpers import GSuiteService, CredentialProvider, GoogleAPIError
from googleapiclient.errors import HttpError

OWNER_ROLE = 'owner'

ORGANIZER_ROLE = 'organizer'

FILE_ORGANIZER_ROLE = 'fileOrganizer'

WRITER_ROLE = 'writer'

COMMENTER_ROLE = 'commenter'

READER_ROLE = 'reader'

ROLES = [OWNER_ROLE, ORGANIZER_ROLE, FILE_ORGANIZER_ROLE, WRITER_ROLE, COMMENTER_ROLE, READER_ROLE]

GRANTEE_USER = 'user'

GRANTEE_GROUP = 'group'

GRANTEE_DOMAIN = 'domain'

GRANTEE_ANYONE = 'anyone'

GRANTEE_TYPES = [GRANTEE_USER, GRANTEE_GROUP, GRANTEE_DOMAIN, GRANTEE_ANYONE]


class DriveService(GSuiteService):
    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('drive', 'v3', credential_provider)

    def create(self, request_id, drive_name):
        body = {
            'name': drive_name
        }
        try:
            result = self.service.drives().create(requestId=request_id, body=body).execute()
            return result
        except HttpError as e:
            raise GoogleAPIError('Unexpected error.', e)

    def get_drive_by_id(self, drive_id):
        result = self.service.drives().get(driveId=drive_id).execute()
        return result

    def list_all_drives(self):
        drives = []
        stop = False
        page_token = None
        while not stop:
            try:
                result = self.service.drives().list(pageToken=page_token).execute()
                drives.extend(result.get('drives', []))
                page_token = result.get('nextPageToken', None)
                stop = page_token is None
            except HttpError as e:
                raise GoogleAPIError('Unexpected error: {}', e)
        return drives

    def list_shared_drive_permissions(self, file_id):
        permissions = []
        stop = False
        page_token = None
        while not stop:
            try:
                result = self.service.permissions().list(fileId=file_id, pageToken=page_token,
                                                         supportsTeamDrives=True).execute()
                permissions.extend(result.get('permissions', []))
                page_token = result.get('nextPageToken', None)
                stop = page_token is None
            except HttpError as e:
                raise GoogleAPIError('Unexpected error: {}', e)
        return permissions

    def add_shared_drive_permission(self, file_id, role, grantee_type, grantee_ref):
        try:
            body = {
                'role': role,
                'type': grantee_type
            }
            if grantee_type == GRANTEE_USER or grantee_type == GRANTEE_GROUP:
                body['emailAddress'] = grantee_ref
            elif grantee_type == GRANTEE_DOMAIN:
                body['domain'] = grantee_ref
            result = self.service.permissions().create(fileId=file_id, supportsTeamDrives=True, body=body).execute()
            return result
        except HttpError as e:
            raise GoogleAPIError('Unexpected error: {}', e)
