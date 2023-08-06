# Copyright (C) 2019 Thomas Hellström <rel@xed.se>
#
# This file is part of ez-gecos.
#
# ez-gecos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ez-gecos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ez-gecos.  If not, see <http://www.gnu.org/licenses/>.

import re
import os


#: ============================================================================
#: GECOS class
#: ============================================================================
class GECOS(object):
    """GECOS

    In the file /etc/passwd there is the so called GECOS field (which stands
    for "General Electric Comprehensive Operating System"), that is:

    username:password:userid:groupid:GECOS:home-dir:shell

    Where GECOS is divided as:

    FullName,RoomAddress,WorkPhone,HomePhone,Others

    ...where others are divided in as many commas as you like:

    FullName,RoomAddress,WorkPhone,HomePhone,Other1,Other2,Other3

    The typical format for the GECOS field is a comma-delimited list with this
    order:

    - User's full name (or application name, if the account is for a program)
    - Building and room number or contact person
    - Office telephone number
    - Home telephone number
    - Any other contact information (pager number, fax, external e-mail
    address, etc.)

    """

    #: ========================================================================
    #: Let's do it!
    #: ========================================================================

    def __init__(self, username: str = None):
        """Lookup a user's GECOS information

        This class tries to parse the GECOS field and exposes the following
        properties:

        - full_name
        - room
        - work_number
        - home_number
        - other
        - email_address (First email address found in 'other')
        - full (The full GECOS field)

        If 'username' is not supplied, parse GECOS field for the username in
        the environment variable 'USER'.
        """

        self._full = None
        self._full_name = None
        self._room = None
        self._work_phone = None
        self._home_phone = None
        self._other = None
        self._email_address = None

        # Default username
        if username is None:
            username = os.environ['USER']

        # We need a string
        if type(username) is not str:
            raise TypeError

        self._username = username

        # Get gecos field for username
        with open('/etc/passwd') as file:
            lines = file.readlines()

        for line in lines:
            if line.startswith(username + ':'):
                self._full = line.split(':')[4]

        # Fill values until we're out of data or silently fail
        # Empty fields will default to 'None' instead of an empty string.
        try:
            c = self._full.split(',')
            self._full_name = c[0] if c[0] else None
            self._room = c[1] if c[1] else None
            self._work_phone = c[2] if c[2] else None
            self._home_phone = c[3] if c[4] else None
            self._other = ','.join(c[4:]) if c[4] else None
        except (AttributeError, IndexError):
            pass

        # Extract first email address from other or silently fail
        try:
            self._email_address = re.findall(
                r'([\w\.-]+@[\w\.-]+\.[\w]+)+', self._other)[0]
        except (IndexError, TypeError):
            pass

    #: ========================================================================
    #: Export our properties
    #: ========================================================================

    @property
    def full_name(self):
        return self._full_name

    @property
    def room(self):
        return self._room

    @property
    def work_phone(self):
        return self._work_phone

    @property
    def home_phone(self):
        return self._home_phone

    @property
    def other(self):
        return self._other

    @property
    def email_address(self):
        return self._email_address

    @property
    def full(self):
        return self._full

    #: ========================================================================
    #: Let's not forget about these!
    #: ========================================================================
    def __str__(self):
        return self._full

    def __repr__(self):
        return f"GECOS(username={self._username})"
