#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from os_vif.internal.command.ip import api


def set(device, check_exit_code=None, state=None, mtu=None, address=None,
        promisc=None, master=None):
    """Method to set a parameter in an interface."""
    return api.ip.set(device, check_exit_code=check_exit_code, state=state,
                      mtu=mtu, address=address, promisc=promisc, master=master)


def add(device, dev_type, check_exit_code=None, peer=None, link=None,
        vlan_id=None, ageing=None):
    """Method to add an interface."""
    return api.ip.add(device, dev_type, check_exit_code=check_exit_code,
                      peer=peer, link=link, vlan_id=vlan_id, ageing=ageing)


def delete(device, check_exit_code=None):
    """Method to delete an interface."""
    return api.ip.delete(device, check_exit_code=check_exit_code)


def exists(device):
    """Method to check if an interface exists."""
    return api.ip.exists(device)
