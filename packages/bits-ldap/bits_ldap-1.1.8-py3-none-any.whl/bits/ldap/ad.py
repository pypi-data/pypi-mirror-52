# -*- coding: utf-8 -*-
"""LDAP Update class for Active Directory."""

import re

from bits.ldap import LDAP as LDAPBase


class AD(LDAPBase):
    """AD LDAP Update class."""

    def __init__(
            self,
            uri,
            bind_dn,
            bind_pw,
            base_dn,
            server_type=None,
            domains=None,
            bitsdb_key=None,
            verbose=False):
        """Initialize a class instance."""
        LDAPBase.__init__(self, uri, bind_dn, bind_pw, base_dn, server_type, domains, bitsdb_key, verbose)

        self.group_attributes = [
            'cn',
            'dSCorePropagationData',
            'description',
            'distinguishedName',
            'gidNumber',
            'groupType',
            'info',
            'instanceType',
            'managedBy',
            'member',
            # 'member;range=0-1499',
            'name',
            'objectCategory',
            'objectClass',
            # 'objectGUID',
            # 'objectSid',
            'sAMAccountName',
            'sAMAccountType',
            'uSNChanged',
            'uSNCreated',
            'whenChanged',
            'whenCreated',
        ]

        self.user_attributes = [
            'accountExpires',
            # 'adminCount',
            # 'badPasswordTime',
            # 'badPwdCount',
            'cn',
            # 'codePage',
            'company',
            # 'countryCode',
            # 'dSCorePropagationData',
            'department',
            'description',
            'directReports',
            'displayName',
            'distinguishedName',
            'division',
            'extensionAttribute11',
            'gidNumber',
            'givenName',
            'homeDirectory',
            'homeDrive',
            'info',
            'initials',
            # 'instanceType',
            # 'lastLogoff',
            # 'lastLogon',
            # 'lastLogonTimestamp',
            # 'lockoutTime',
            'loginShell',
            # 'logonCount',
            # 'logonHours',
            'mail',
            'managedObjects',
            'manager',
            'maxPwdAge',
            'member',
            'memberOf',
            'msRADIUSCallbackNumber',
            'msRADIUSFramedIPAddress',
            'msRADIUSServiceType',
            # 'msTSExpireDate',
            # 'msTSLicenseVersion',
            # 'msTSLicenseVersion2',
            # 'msTSLicenseVersion3',
            # 'msTSManagingLS',
            'name',
            'objectCategory',
            # 'objectClass',
            # 'objectGUID',
            # 'objectSid',
            'physicalDeliveryOfficeName',
            'primaryGroupID',
            'profilePath',
            'pwdLastSet',
            'sAMAccountName',
            'sAMAccountType',
            # 'scriptPath'
            'sn',
            'telephoneNumber',
            # 'terminalServer'
            'title',
            # 'uSNChanged',
            # 'uSNCreated',
            'uid',
            'uidNumber',
            'unixHomeDirectory',
            'userAccountControl',
            # 'userCertificate',
            'userPrincipalName',
            'whenChanged',
            'whenCreated',
        ]

        self.groups = {}
        self.users = {}
        self.users_by_dn = {}

    #
    # Helpers
    #
    def get_expire_date(self, maxDays=None):
        """Convert pwd last set date to a datetime."""
        """TODO"""

    def get_pwd_last_set_date(self, last):
        """Convert pwd last set date to an expiration date."""
        """TODO"""
    #
    # Groups
    #
    def check_group(self, groupname):
        """Check if an Active Directory group exists."""
        try:
            if self.get_group(groupname):
                return True
        except Exception:
            return False

    def get_group(self, groupname, bytes_mode=True):
        """Return a single group."""
        filterstr = '(sAMAccountName={})'.format(groupname)

        # bytes mode
        if bytes_mode:
            entries = self.get_entries(filterstr, self.group_attributes)
            for dn in entries:
                return entries[dn]

        # unicode strings mode
        entries = self.get_entries(filterstr, self.group_attributes)
        for dn in entries:
            return self.convert_entry_to_strings(entries[dn])

    def get_groups(self, attrlist=None, bytes_mode=True, key='sAMAccountName'):
        """Return a dict of groups by groupname."""
        entries = self.get_groups_by_dn(attrlist=attrlist, bytes_mode=bytes_mode)
        groups = {}
        for dn in entries:
            e = entries[dn]
            k = e[key][0]
            if isinstance(k, bytes):
                k = k.decode('utf-8')
            groups[k] = e
        return groups

    def get_groups_by_dn(self, attrlist=None, bytes_mode=True):
        """Return a dict of groups from Active Directory."""
        filterstr = '(&(objectCategory=group)(sAMAccountName=*))'

        if not attrlist:
            attrlist = self.user_attributes

        # bytes mode
        if bytes_mode:
            return self.get_entries(filterstr, self.user_attributes)

        # unicode strings mode
        entries = self.get_entries(filterstr, self.user_attributes)
        groups = {}
        for dn in entries:
            groups[dn] = self.convert_entry_to_strings(entries[dn])
        return groups

    def get_groups_by_gid(self, bytes_mode=True):
        """Return a dict of groups by gid."""
        groups = self.get_groups(bytes_mode=bytes_mode)
        gid_groups = {}
        for groupname in groups:
            g = groups[groupname]
            if 'gidNumber' in g and g['gidNumber'] and int(g['gidNumber'][0]) >= 0:
                gid = int(g['gidNumber'][0])
                if gid in gid_groups:
                    gid_groups[gid] = [groupname]
                else:
                    gid_groups[gid] = [groupname]
        return gid_groups

    def get_groups_by_username(self, bytes_mode=True):
        """Return a dict of groups by username."""
        groups = self.get_groups_for_nis()
        user_groups = {}
        for groupname in groups:
            g = groups[groupname]
            members = g['users']
            for m in members:
                if not m:
                    continue
                if m not in user_groups:
                    user_groups[m] = []
                user_groups[m].append(groupname)

        return user_groups

    def get_groups_for_nis(self, bytes_mode=True, people=None):
        """Return a dict of groups for NIS."""
        groups = self.get_groups(bytes_mode=False)
        users = self.get_users_by_dn(bytes_mode=False)

        nis_groups = {}
        notfound = []
        for groupname in groups:
            g = groups[groupname]

            # only get groups that have a gid
            if 'gidNumber' not in g or int(g['gidNumber'][0]) < 0:
                continue

            gid = int(g['gidNumber'][0])

            members = []

            # see if the group has members:
            if 'member' in g:

                # cycle through the members
                for m in g['member']:

                    # skip users without a dn
                    if not m:
                        continue

                    # check if user exists in AD
                    if m in users:
                        u = users[m]

                        # set the username
                        username = u['sAMAccountName'][0].lower()

                        if people and username in people and people[username]['terminated']:
                            continue

                        # add the username to the list of members
                        members.append(username)

                    else:
                        print('ERROR: AD user not found!: {} ({})'.format(m, groupname))
                        notfound.append(m)

            data = {
                'name': groupname,
                'gid': gid,
                'password': '*',
                'users': members,
            }

            nis_groups[groupname] = data

        return nis_groups

    def update_group(self, auth):
        """Update a single group in Active Directory."""
        """TODO"""

    def update_groups(self, auth):
        """Update groups in Active Directory."""
        group_syncs = [
            'bits',
            'dialpad_users',
            'dsp',
            'engineering',
            'genomicsplatform',
            'getz_lab',
            'gtexadmin',
            'operations',
            'ops_interns',
            'uger',
        ]

        #
        # Update specific AD group
        #
        def bits(auth):
            """Update BITS group from Google."""
            groupname = 'bits'
            users = self.get_google_group_members(groupname, auth)
            self.update_group_members(groupname, users)

        def dialpad_users(auth):
            """Update dialpad users group from Google."""
            groupname = 'dialpad-users'
            users = self.get_google_group_members(groupname, auth)
            self.update_group_members(groupname, users)

        def dsp(auth):
            """Update DSP group from ADP."""
            p = auth.people()

            people = p.getPeople()
            users = []
            for pid in people:
                person = people[pid]

                orgunit = person['org_unit']
                person_type = person['person_type_name']
                terminated = person['terminated']
                username = person['username']

                if terminated:
                    continue

                if person_type in ['Non-Partner Institution']:
                    continue

                if re.search('Data Sciences Platform', orgunit):
                    users.append(username)

            self.update_group_members('Data Sciences Platform', users)

        def engineering(auth):
            """Update engineering group from Google."""
            groupname = 'engineering'
            users = self.get_google_group_members(groupname, auth)
            self.update_group_members(groupname, users)

        def genomicsplatform(auth):
            """Update the genomicsplatform group from ADP."""
            p = auth.people()
            people = p.getPeople()
            users = []
            for pid in people:
                person = people[pid]

                orgunit = person['org_unit']
                person_type = person['person_type_name']
                terminated = person['terminated']
                username = person['username']

                if terminated:
                    continue

                if person_type in ['Non-Partner Institution']:
                    continue

                if re.search('Genomics Platform', orgunit):
                    users.append(username)

            self.update_group_members('Genomics Platform', users)

        def getz_lab(auth):
            """Update getz-lab group from Google."""
            groupname = 'getz-lab'
            users = self.get_google_group_members(groupname, auth)
            self.update_group_members(groupname, users)

        def gtexadmin(auth):
            """Update the GTEX Admin AD Group."""
            g = auth.google()
            g.auth_service_account(g.scopes, g.subject)
            members = g.directory().get_members('gtex-admin@broadinstitute.org')
            users = []
            for m in members:
                email = m['email']
                if re.search('@broadinstitute.org$', email):
                    users.append(email.replace('@broadinstitute.org', ''))
            self.update_group_members('gtex-admin', users)

        def operations(auth):
            """Update operations group from Google."""
            groupname = 'operations'
            users = self.get_google_group_members(groupname, auth)
            self.update_group_members(groupname, users)

        def ops_interns(auth):
            """Update operations group from Google."""
            groupname = 'ops-interns'
            users = self.get_google_group_members(groupname, auth)
            self.update_group_members(groupname, users)

        def uger(auth):
            """Update the Uger groups in AD."""
            g = auth.google()
            g.auth_service_account(g.scopes, g.subject)
            m = auth.mongo()

            uger_groups = m.getCollection('uger_group_sync')
            for oid in sorted(uger_groups, key=lambda x: uger_groups[x]['google_group_email']):
                uger_group = uger_groups[oid]
                group_email = uger_group['google_group_email']
                group_name = uger_group['google_group_name'].replace('-', '_')

                if auth.verbose:
                    print('Syncing group: %s' % (group_email))

                members = g.directory().get_members(group_email)
                users = []
                for m in members:
                    email = m['email']
                    if re.search('@broadinstitute.org$', email):
                        users.append(email.replace('@broadinstitute.org', ''))
                self.update_group_members(group_name, users)

        #
        # Update AD Groups
        #
        users = self.get_users(bytes_mode=False)
        print('Updating AD group members from Google Groups...')
        for groupname in sorted(group_syncs):
            """Do stuff."""
            print('Updating Group: {}'.format(groupname))
            locals()[groupname](auth)

    #
    # Members
    #
    def add_group_member(self, groupname, username):
        """Add a user to an Active Directory group."""
        group = self.get_group(groupname, bytes_mode=False)
        if not group:
            print('ERROR: No such group: {}'.format(groupname))
            return

        user = self.get_user(username, bytes_mode=False)
        if not user:
            print('ERROR: No such user: {}'.format(username))
            return

        # get dns
        groupDn = group['distinguishedName'][0]
        userDn = user['distinguishedName'][0]

        # check if group has any members
        if 'member' not in group:
            group['member'] = []

        # check if user is already in group
        if userDn in group['member']:
            return True

        modlist = [(self.ldapmodule.MOD_ADD, 'member', userDn.encode('utf-8'))]
        return self.ldapobject.modify_s(groupDn, modlist)

    def get_google_group_members(self, groupname, auth):
        """Return the members from a Google Group for syncing with AD."""
        g = auth.google()
        g.auth_service_account(g.scopes, g.subject)

        # add domain name
        email = groupname
        if not re.search('@', groupname):
            email = '%s@broadinstitute.org' % (groupname)

        # get members
        members = g.directory().get_members_recursively(email)

        # create users list
        users = []
        for m in members:
            user = m['email']
            if re.search('@broadinstitute.org', user):
                user = user.replace('@broadinstitute.org', '')
            users.append(user)
        return users

    def remove_group_member(self, groupname, username):
        """Remove a user from an Active Directory group."""
        group = self.get_group(groupname, bytes_mode=False)
        if not group:
            print('ERROR: No such group: {}'.format(groupname))
            return

        user = self.get_user(username, bytes_mode=False)
        if not user:
            print('ERROR: No such user: {}'.format(username))
            return

        # get dns
        groupDn = group['distinguishedName'][0]
        userDn = user['distinguishedName'][0]

        # check if group has any members
        if 'member' not in group:
            group['member'] = []

        # check if user is already in group
        if userDn not in group['member']:
            return True

        modlist = [(self.ldapmodule.MOD_DELETE, 'member', userDn.encode('utf-8'))]
        return self.ldapobject.modify_s(groupDn, modlist)

    def update_group_members(self, groupname, groupusers):
        """Update the members of an Active Directory groups."""
        group = self.get_group(groupname, bytes_mode=False)

        if 'member' not in group:
            members = []
        else:
            members = group['member']

        # find members to add
        add = []
        for username in sorted(groupusers):
            if username not in self.users:
                print('ERROR: AD username not found [%s]: %s' % (
                    groupname,
                    username,
                ))
                continue

            user = self.users[username]
            dn = user['distinguishedName'][0]
            if dn not in members:
                add.append(username)

        # find members to remove
        remove = []
        for dn in sorted(members):
            if dn not in self.users_by_dn:
                print('ERROR: AD user DN not found [%s]: %s' % (
                    groupname,
                    dn
                ))
                continue

            user = self.users_by_dn[dn]
            username = user['sAMAccountName'][0]
            if username not in groupusers:
                remove.append(username)

        if add or remove:
            print('Updating AD group: %s' % (groupname))

        # add users
        if add:
            print('  Adding users:')
            for username in sorted(add):
                print('   + %s' % (username))
                self.add_group_member(groupname, username)

        # remove users
        if remove:
            print('  Removing users:')
            for username in sorted(remove):
                print('   - %s' % (username))
                self.remove_group_member(groupname, username)

    #
    # OUs
    #
    def get_ous(self, bytes_mode=True):
        """Return a dict of ous from Active Directory."""
        attrlist = ['ou']
        filterstr = '(ou=*)'

        # bytes mode
        if bytes_mode:
            return self.get_entries(filterstr, attrlist)

        # unicode strings mode
        entries = self.get_entries(filterstr, attrlist)
        ous = {}
        for dn in entries:
            ous[dn] = self.convert_entry_to_strings(entries[dn])
        return ous

    #
    # Users
    #
    def check_user(self, username):
        """Check if an Active Directory user exists."""
        try:
            if self.get_user(username):
                return True
        except Exception:
            return False

    def create_user(self, username):
        """Create a user in Active Directory."""
        """TODO"""

    def delete_user(self, username):
        """Delete a user in Active Directory."""
        user = self.get_user(username, bytes_mode=False)
        if not user:
            print('ERROR: No such user: {}'.format(username))
            return

        # get dn
        dn = user['distinguishedName'][0]

        # delete user
        self.ldapmodule.delete_entry(dn)

        return user

    def get_user(self, username, bytes_mode=True):
        """Return a single user."""
        filterstr = '(sAMAccountName={})'.format(username)

        # bytes mode
        if bytes_mode:
            entries = self.get_entries(filterstr, self.user_attributes)
            for dn in entries:
                return entries[dn]

        # unicode strings mode
        entries = self.get_entries(filterstr, self.user_attributes)
        for dn in entries:
            return self.convert_entry_to_strings(entries[dn])

    def get_users(self, attrlist=None, bytes_mode=True, key='sAMAccountName'):
        """Return a dict of users by username."""
        entries = self.get_users_by_dn(attrlist=attrlist, bytes_mode=bytes_mode)
        users = {}
        for dn in entries:
            e = entries[dn]
            k = e[key][0]
            if isinstance(k, bytes):
                k = k.decode('utf-8')
            users[k] = e
        self.users = users
        return users

    def get_users_by_dn(self, attrlist=None, bytes_mode=True):
        """Return a dict of users from Active Directory."""
        filterstr = '(&(objectCategory=person)(sAMAccountName=*))'

        if not attrlist:
            attrlist = self.user_attributes

        # bytes mode
        if bytes_mode:
            return self.get_entries(filterstr, attrlist)

        # unicode strings mode
        entries = self.get_entries(filterstr, attrlist)
        users = {}
        for dn in entries:
            users[dn] = self.convert_entry_to_strings(entries[dn])
        self.users_by_dn = users
        return users

    def get_users_for_nis(self):
        """Return a dict of users for NIS."""
        users = self.get_users(bytes_mode=False)
        nis_users = {}
        for username in sorted(users):
            if not username:
                continue

            u = users[username]

            if not u:
                print('ERROR: AD user not found: %s' % (username))
                continue

            if 'uidNumber' not in u or int(u['uidNumber'][0]) < 0:
                continue

            if 'gidNumber' not in u or int(u['gidNumber'][0]) < 0:
                continue

            if 'loginShell' not in u or not str(u['loginShell'][0]):
                continue

            if 'unixHomeDirectory' not in u or not str(u['unixHomeDirectory'][0]):
                continue

            uid = int(u['uidNumber'][0])
            gid = int(u['gidNumber'][0])
            home_dir = u['unixHomeDirectory'][0]
            shell = u['loginShell'][0]
            gecos = u['displayName'][0]

            user = {
                'username': username,
                'uid': uid,
                'gid': gid,
                'gecos': gecos,
                'password': '*',
                'shell': shell,
                'home_dir': home_dir,
            }

            nis_users[username] = user

        return nis_users

    def lock_user(self, username):
        """Lock a user in Active Directory."""
        """TODO"""

    def move_user(self, username, newParent):
        """Move a user in Active Directory."""
        user = self.get_user(username, bytes_mode=False)
        if not user:
            print('ERROR: No such user: {}'.format(username))
            return

        dn = user['distinguishedName'][0]
        rdn = 'CN={}'.format(user['cn'][0])
        self.ldapmodule.rename_s(dn, rdn, newParent)

    def prepare_user(self):
        """Prepare a single user for in Active Directory."""
        """TODO"""

    def rename_user(self, username, newRdn):
        """Rename a user in Active Directory."""
        user = self.get_user(username, bytes_mode=False)
        if not user:
            print('ERROR: No such user: {}'.format(username))
            return

        dn = user['distinguishedName'][0]
        self.ldapmodule.rename_s(dn, newRdn)

    def set_password(self, username):
        """Set a user's password in Active Directory."""
        """TODO"""

    def unlock_user(self, username):
        """Unlock a user in Active Directory."""
        """TODO"""

    def update_user(self):
        """Update a single user in Active Directory."""
        """TODO"""

    def update_users(self):
        """Update users in Active Directory."""
        """TODO"""
