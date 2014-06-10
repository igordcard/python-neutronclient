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

import logging
import string

from neutronclient.neutron import v2_0 as neutronv20
from neutronclient.openstack.common.gettextutils import _


class ListPortChain(neutronv20.ListCommand):
    """List port chains that belong to a given tenant."""

    resource = 'port_chain'
    log = logging.getLogger(__name__ + '.ListPortChain')
    list_columns = ['id', 'name', 'description']
    pagination_support = True
    sorting_support = True


class ShowPortChain(neutronv20.ShowCommand):
    """Show information of a given port chain."""

    resource = 'port_chain'
    log = logging.getLogger(__name__ + '.ShowPortChain')


class CreatePortChain(neutronv20.CreateCommand):
    """Create a port chain."""

    resource = 'port_chain'
    log = logging.getLogger(__name__ + '.CreatePortChain')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            help=_('Name for the port chain'))
        parser.add_argument(
            '--description',
            help=_('Description for the port chain'))
        parser.add_argument(
            '--ports',
            action='append',
            #type=string.split,
            help=_('Ports to chain'))
        parser.add_argument(
            '--classifiers', type=string.split,
            help=_('List of whitespace-delimited classifier name or IDs; '
                   'e.g., --classifiers \"classifier1 classifier2\"'))

    def args2body(self, parsed_args):
        body = {self.resource: {}, }
        if parsed_args.classifiers:
            _classifiers = []
            for c in parsed_args.classifiers:
                _classifiers.append(
                    neutronv20.find_resourceid_by_name_or_id(
                        self.get_client(), 'steering_classifier', c))
            body[self.resource]['steering_classifiers'] = _classifiers
	# FIXME(cgoncalves): the following commented lines regards the
	#                    dict(list(uuid)) approach
        #_ports = {}
        #if parsed_args.ports:
            #for port_chain in parsed_args.ports:
            #    port_group = port_chain.split(':')
            #	src_port = port_group[0]
            #	dst_ports = port_group[1:][0]
            #    _ports[src_port] = [p for p in dst_ports.split(',')]
        #body[self.resource]['ports'] = _ports
        _ports = []
        if parsed_args.ports:
            for port_group in parsed_args.ports:
                _ports.append(port_group.split(','))
        body[self.resource]['ports'] = _ports
        neutronv20.update_dict(parsed_args, body[self.resource],
                               ['name', 'description', 'steering_classifiers'])
        return body


class DeletePortChain(neutronv20.DeleteCommand):
    """Delete a port chain."""

    resource = 'port_chain'
    log = logging.getLogger(__name__ + '.DeletePortChain')


class UpdatePortChain(neutronv20.UpdateCommand):
    """Update a port chain."""

    resource = 'port_chain'
    log = logging.getLogger(__name__ + '.UpdatePortChain')
