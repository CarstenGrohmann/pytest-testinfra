# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from testinfra.modules.base import Module


class Group(Module):
    """Test unix group"""

    def __init__(self, name):
        self.name = name
        super().__init__()

    @property
    def exists(self):
        """Test if the group exists

        >>> host.group("wheel").exists
        True
        >>> host.group("nosuchgroup").exists
        False
        """
        return self.run_expect([0, 2], "getent group %s", self.name).rc == 0

    @property
    def get_all_groups(self):
        """Returns a list of local and remote group names

        >>> host.group("anyname").get_all_groups
        ["root", "wheel", "man", "tty", <...>]
        """
        all_groups = [
            line.split(":")[0]
            for line in self.check_output("getent group").splitlines()
        ]
        return all_groups

    @property
    def get_local_groups(self):
        """Returns a list of local group names

        >>> host.group("anyname").get_local_groups
        ["root", "wheel", "man", "tty", <...>]
        """
        local_groups = [
            line.split(":")[0]
            for line in self.check_output("cat /etc/group").splitlines()
        ]
        return local_groups

    @property
    def gid(self):
        return int(self.check_output("getent group %s | cut -d':' -f3", self.name))

    @property
    def members(self):
        """Return all users that are members of this group."""
        users = self.check_output("getent group %s | cut -d':' -f4", self.name)
        if users:
            return users.split(",")
        return []

    def __repr__(self):
        return f"<group {self.name}>"
