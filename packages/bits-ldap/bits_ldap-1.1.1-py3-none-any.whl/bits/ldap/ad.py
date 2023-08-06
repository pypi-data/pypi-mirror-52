"""LDAP Update class for Active Directory."""


class AD(object):
    """AD LDAP Update class."""

    def __init__(self, ldap):
        """Initialize a class instance."""
        self.ldap = ldap

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
            entries = self.ldap.get_entries(filterstr, self.group_attributes)
            for dn in entries:
                return entries[dn]

        # unicode strings mode
        entries = self.ldap.get_entries(filterstr, self.group_attributes)
        for dn in entries:
            return self.ldap.convert_entry_to_strings(entries[dn])

    def get_groups(self, bytes_mode=True):
        """Return a dict of groups by groupname."""
        entries = self.get_groups_by_dn(bytes_mode=bytes_mode)
        groups = {}
        for dn in entries:
            e = entries[dn]
            groupname = e['cn'][0]
            if isinstance(groupname, bytes):
                groupname = groupname.decode('utf-8')
            groups[groupname] = e
        return groups

    def get_groups_by_dn(self, bytes_mode=True):
        """Return a dict of groups from Active Directory."""
        filterstr = '(&(objectCategory=group)(sAMAccountName=*))'

        # bytes mode
        if bytes_mode:
            return self.ldap.get_entries(filterstr, self.user_attributes)

        # unicode strings mode
        entries = self.ldap.get_entries(filterstr, self.user_attributes)
        groups = {}
        for dn in entries:
            groups[dn] = self.ldap.convert_entry_to_strings(entries[dn])
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

    def update_group(self):
        """Update a single group in Active Directory."""
        """TODO"""

    def update_groups(self):
        """Update groups in Active Directory."""
        """TODO"""

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

        modlist = [(self.ldap.ldapmodule.MOD_ADD, 'member', userDn.encode('utf-8'))]
        return self.ldap.ldapobject.modify_s(groupDn, modlist)

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

        modlist = [(self.ldap.ldapmodule.MOD_DELETE, 'member', userDn.encode('utf-8'))]
        return self.ldap.ldapobject.modify_s(groupDn, modlist)

    def update_group_members(self, groupname, members):
        """Update the members of an Active Directory groups."""
        """TODO"""

    #
    # OUs
    #
    def get_ous(self, bytes_mode=True):
        """Return a dict of ous from Active Directory."""
        attrlist = ['ou']
        filterstr = '(ou=*)'

        # bytes mode
        if bytes_mode:
            return self.ldap.get_entries(filterstr, attrlist)

        # unicode strings mode
        entries = self.ldap.get_entries(filterstr, attrlist)
        ous = {}
        for dn in entries:
            ous[dn] = self.ldap.convert_entry_to_strings(entries[dn])
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
        self.ldap.delete_entry(dn)

        return user

    def get_user(self, username, bytes_mode=True):
        """Return a single user."""
        filterstr = '(sAMAccountName={})'.format(username)

        # bytes mode
        if bytes_mode:
            entries = self.ldap.get_entries(filterstr, self.user_attributes)
            for dn in entries:
                return entries[dn]

        # unicode strings mode
        entries = self.ldap.get_entries(filterstr, self.user_attributes)
        for dn in entries:
            return self.ldap.convert_entry_to_strings(entries[dn])

    def get_users(self, bytes_mode=True):
        """Return a dict of users by username."""
        entries = self.get_users_by_dn(bytes_mode=bytes_mode)
        users = {}
        for dn in entries:
            e = entries[dn]
            username = e['cn'][0]
            if isinstance(username, bytes):
                username = username.decode('utf-8')
            users[username] = e
        return users

    def get_users_by_dn(self, bytes_mode=True):
        """Return a dict of users from Active Directory."""
        filterstr = '(&(objectCategory=person)(sAMAccountName=*))'

        # bytes mode
        if bytes_mode:
            return self.ldap.get_entries(filterstr, self.user_attributes)

        # unicode strings mode
        entries = self.ldap.get_entries(filterstr, self.user_attributes)
        users = {}
        for dn in entries:
            users[dn] = self.ldap.convert_entry_to_strings(entries[dn])
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
        self.ldap.rename_s(dn, rdn, newParent)

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
        self.ldap.rename_s(dn, newRdn)

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
