# Copyright 2014 OpenStack Foundation.
# All Rights Reserved
#
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

import sys

from neutronclient.neutron.v2_0.ts import port_chain
from neutronclient.tests.unit import test_cli20


class CLITestV20PortChainJSON(test_cli20.CLITestV20Base):

    def test_create_port_chain_with_all_params(self):
        resource = 'port_chain'
        cmd = port_chain.CreatePortChain(test_cli20.MyApp(sys.stdout), None)
        name = 'mychain'
        my_id = 'myid'
        description = 'chain description'
        ports = ['port1', 'port2', 'port3']
        classifier1 = 'classifier1'
        classifier2 = 'classifier2'
        classifiers = [classifier1, classifier2]

        args = ['--name', name,
                '--description', description,
                '--ports', ports,
                '--classifiers', 'classifier1 classifier2', ]
        position_names = ['name', 'description', 'ports', 'classifiers', ]
        position_values = [name, description, ports, classifiers, ]
        self._test_create_resource(resource, cmd, name, my_id, args,
                                   position_names, position_values)

    def test_list_port_chains(self):
        resources = 'port_chains'
        cmd = port_chain.ListPortChain(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, True)

    def test_list_port_chains_pagination(self):
        resources = 'port_chains'
        cmd = port_chain.ListPortChain(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources_with_pagination(resources, cmd)

    def test_list_port_chains_sort(self):
        resources = 'port_chains'
        cmd = port_chain.ListPortChain(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd,
                                  sort_key=['name', 'id'],
                                  sort_dir=['asc', 'desc'])

    def test_list_port_chains_limit(self):
        resources = 'port_chains'
        cmd = port_chain.ListPortChain(test_cli20.MyApp(sys.stdout), None)
        self._test_list_resources(resources, cmd, page_size=1000)

    def test_show_port_chain_id(self):
        resource = 'port_chain'
        cmd = port_chain.ShowPortChain(test_cli20.MyApp(sys.stdout), None)
        args = ['--fields', 'id', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id, args, ['id'])

    def test_show_port_chain_id_name(self):
        resource = 'port_chain'
        cmd = port_chain.ShowPortChain(test_cli20.MyApp(sys.stdout), None)
        args = ['--fields', 'id', '--fields', 'name', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id,
                                 args, ['id', 'name'])

    def test_update_port_chain(self):
        resource = 'port_chain'
        cmd = port_chain.UpdatePortChain(test_cli20.MyApp(sys.stdout), None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['myid', '--name', 'myname', ],
                                   {'name': 'myname', })

    def test_delete_port_chain(self):
        resource = 'port_chain'
        cmd = port_chain.DeletePortChain(test_cli20.MyApp(sys.stdout), None)
        my_id = 'my-id'
        args = [my_id]
        self._test_delete_resource(resource, cmd, my_id, args)


class CLITestV20PortChainXML(CLITestV20PortChainJSON):
    format = 'xml'
