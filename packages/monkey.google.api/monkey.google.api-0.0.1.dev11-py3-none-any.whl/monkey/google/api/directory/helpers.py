#!/usr/bin/python
# -*- coding: utf-8 -*-

from monkey.google.api.helpers import GSuiteService, CredentialProvider, GoogleAPIError
from googleapiclient.errors import HttpError

GROUP_MEMBER_ROLE = 'MEMBER'

GROUP_OWNER_ROLE = 'OWNER'

GROUP_MANAGER_ROLE = 'MANAGER'

GROUP_MEMBER_ROLES = [GROUP_MEMBER_ROLE, GROUP_MANAGER_ROLE, GROUP_OWNER_ROLE]

DELIVERY_SETTINGS_NONE = 'NONE'

DELIVERY_SETTINGS_DISABLED = 'DISABLED'

DELIVERY_SETTINGS_DIGEST = 'DIGEST'

DELIVERY_SETTINGS_DAILY = 'DAILY'

DELIVERY_SETTINGS_ALL = 'ALL_MAIL'

DELIVERY_SETTINGS = [DELIVERY_SETTINGS_ALL, DELIVERY_SETTINGS_DAILY, DELIVERY_SETTINGS_DIGEST,
                     DELIVERY_SETTINGS_DISABLED, DELIVERY_SETTINGS_NONE]


class DirectoryService(GSuiteService):

    def __init__(self, credential_provider: CredentialProvider):
        super().__init__('admin', 'directory_v1', credential_provider)

    def list_all(self):
        raise NotImplemented()


class DirectoryGroupService(DirectoryService):

    def __init__(self, credential_provider: CredentialProvider):
        super().__init__(credential_provider)

    def list_all(self):
        groups = []
        stop = False
        page_token = None
        while not stop:
            result = self.service.groups().list(customer='my_customer', orderBy='email',
                                                sortOrder='DESCENDING', pageToken=page_token).execute()
            groups.extend(result.get('groups', []))
            page_token = result.get('nextPageToken', None)
            stop = page_token is None
        return groups

    def get_members(self, group_key):
        members = []
        stop = False
        page_token = None
        while not stop:
            result = self.service.members().list(groupKey=group_key, pageToken=page_token).execute()
            members.extend(result.get('user_members', []))
            page_token = result.get('nextPageToken', None)
            stop = page_token is None
        return members

    def create(self, name, email_addr, desc):
        group_def = {'email': email_addr,
                     'name': name,
                     'description': desc}
        created_group = self.service.groups().insert(body=group_def).execute()
        return created_group

    def update(self, group_key, name, email_addr, desc):
        group_def = {'email': email_addr,
                     'name': name,
                     'description': desc}
        updated_group = self.service.groups().update(groupKey=group_key, body=group_def).execute()
        return updated_group

    def find_by_email_addr(self, email_addr):
        groups = []
        stop = False
        page_token = None
        query_str = 'email:{}*'.format(email_addr)
        while not stop:
            try:
                result = self.service.groups().list(customer='my_customer', maxResults=1, orderBy='email',
                                                    sortOrder='ASCENDING', query=query_str,
                                                    pageToken=page_token).execute()
                groups.extend(result.get('groups', []))
                page_token = result.get('nextPageToken', None)
                stop = page_token is None
            except Exception as e:
                raise GoogleAPIError('Unexpected error: {}', e)
        return groups

    def list_aliases(self, group_key):
        aliases = []
        try:
            result = self.service.groups().aliases().list(groupKey=group_key).execute()
            aliases.extend(result.get('aliases', []))
        except Exception as e:
            raise GoogleAPIError('Unexpected error: {}', e)
        return aliases

    def add_aliases(self, group_key, aliases):
        success = []
        errors = []
        for alias in aliases:
            if len(alias.strip()) > 0:
                try:
                    body = {'alias': alias}
                    result = self.service.groups().aliases().insert(groupKey=group_key, body=body).execute()
                    success.append(alias)
                except HttpError as e:
                    self.logger.error('Failed to insert alias {} on group {}.'.format(alias, group_key))
                    errors.append(alias)
        return success, errors

    def delete_aliases(self, group_key, aliases):
        success = []
        errors = []
        for alias in aliases:
            if len(alias.strip()) > 0:
                try:
                    result = self.service.groups().aliases().delete(groupKey=group_key, alias=alias).execute()
                    success.append(alias)
                except HttpError as e:
                    self.logger.error('Failed to delete alias {} from group {}.'.format(alias, group_key))
                    errors.append(alias)
        return success, errors

    def update_aliases(self, group_key, aliases):
        old_aliases = self.list_aliases(group_key)
        new_aliases = []
        new_aliases.extend(aliases)
        old_aliases_to_delete = []
        for old_alias in old_aliases:
            old_alias_email_addr = old_alias['alias']
            if old_alias_email_addr in aliases:
                new_aliases.remove(old_alias_email_addr)
            else:
                old_aliases_to_delete.append(old_alias_email_addr)
        # Delete unwanted old aliases
        del_success, del_errors = self.delete_aliases(group_key, old_aliases_to_delete)
        # Add new aliases
        add_success, add_errors = self.add_aliases(group_key, new_aliases)
        return (add_success, del_success), (add_errors, del_errors)

    def list_members(self, group_key):
        members = []
        stop = False
        page_token = None
        while not stop:
            try:
                result = self.service.members().list(groupKey=group_key, pageToken=page_token).execute()
                members.extend(result.get('members', []))
                page_token = result.get('nextPageToken', None)
                stop = page_token is None
            except HttpError as e:
                raise GoogleAPIError('Unexpected error: {}', e)
        return members

    def add_members(self, group_key, member_keys, role=GROUP_MEMBER_ROLE, delivery_settings=DELIVERY_SETTINGS_ALL):
        success = []
        errors = []
        for member_key in member_keys:
            try:
                body = {
                    'email': member_key,
                    'role': role,
                    'delivery_settings': delivery_settings
                }
                result = self.service.members().insert(groupKey=group_key, body=body).execute()
                success.append(member_key)
            except HttpError as e:
                self.logger.error('Failed to add member {} on group {}.'.format(member_key, group_key))
                errors.append(member_key)
        return success, errors

    def add_member(self, group_key, member_key, role=GROUP_MEMBER_ROLE, delivery_settings=DELIVERY_SETTINGS_ALL):
        try:
            body = {
                'email': member_key,
                'role': role,
                'delivery_settings': delivery_settings
            }
            result = self.service.members().insert(groupKey=group_key, body=body).execute()
            return result
        except HttpError as e:
            raise GoogleAPIError('Failed to add member {} on group {}.'.format(member_key, group_key), e)

    def delete_members(self, group_key, member_keys):
        success = []
        errors = []
        for member_key in member_keys:
            try:
                result = self.service.members().delete(groupKey=group_key, memberKey=member_key).execute()
                success.append(member_key)
            except HttpError as e:
                self.logger.error('Failed to delete member {} from group {}.'.format(member_key, group_key))
                errors.append(member_key)
        return success, errors

    def update_members(self, group_key, members, role=GROUP_MEMBER_ROLE, delivery_settings=DELIVERY_SETTINGS_ALL):
        old_members = self.list_members(group_key)
        new_members = []
        new_members.extend(members)
        old_members_to_delete = []
        for old_members in old_members:
            old_member_email_addr = old_members['email']
            if old_member_email_addr in members:
                new_members.remove(old_member_email_addr)
            else:
                old_members_to_delete.append(old_member_email_addr)
        # Delete unwanted old members
        del_success, del_errors = self.delete_members(group_key, old_members_to_delete)
        # Add new members
        add_success, add_errors = self.add_members(group_key, new_members, role, delivery_settings)
        return (add_success, del_success), (add_errors, del_errors)

    def update_member(self, group_key, member_key, role=GROUP_MEMBER_ROLE, delivery_settings=DELIVERY_SETTINGS_ALL):
        try:
            body = {
                'role': role,
                'delivery_settings': delivery_settings
            }
            result = self.service.members().update(groupKey=group_key, member_key=member_key, body=body).execute()
            return result
        except HttpError as e:
            raise GoogleAPIError('Failed to add member {} on group {}.'.format(member_key, group_key), e)


class DirectoryUserService(DirectoryService):

    def __init__(self, credential_provider: CredentialProvider):
        super().__init__(credential_provider)

    def list_all(self):
        users = []
        stop = False
        page_token = None
        while not stop:
            result = self.service.users().list(customer='my_customer', orderBy='email',
                                               sortOrder='ASCENDING', pageToken=page_token).execute()
            users.extend(result.get('users', []))
            page_token = result.get('nextPageToken', None)
            stop = page_token is None
        return users

    def find(self, query_str):
        users = []
        stop = False
        page_token = None
        try:
            while not stop:
                result = self.service.users().list(customer='my_customer', orderBy='email', sortOrder='ASCENDING',
                                                   query=query_str, pageToken=page_token).execute()

                users.extend(result.get('users', []))
                page_token = result.get('nextPageToken', None)
                stop = page_token is None
        except HttpError as e:
            raise GoogleAPIError('Unexpected error.', e)
        return users

    def find_by_ou_path(self, ou_path):
        query_str = 'orgUnitPath={}'.format(ou_path)
        return self.find(query_str)

    def find_by_email_addr(self, email_addr):
        query_str = 'email={}'.format(email_addr)
        users = self.find(query_str)
        return users[0]
