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

from neutronclient.neutron import v2_0 as neutronv20
from neutronclient.openstack.common.gettextutils import _


class ListSteeringClassifier(neutronv20.ListCommand):
    """List traffic steering classifiers that belong to a given tenant."""

    resource = 'steering_classifier'
    log = logging.getLogger(__name__ + '.ListSteeringTraffic')
    list_columns = ['id', 'name', 'description']
    pagination_support = True
    sorting_support = True


class ShowSteeringClassifier(neutronv20.ShowCommand):
    """Show information of a given classifier."""

    resource = 'steering_classifier'
    log = logging.getLogger(__name__ + '.ShowSteeringClassifier')


class CreateSteeringClassifier(neutronv20.CreateCommand):
    """Create a traffic steering classifier."""

    resource = 'steering_classifier'
    log = logging.getLogger(__name__ + '.CreateSteeringClassifier')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            help=_('Name for the firewall rule'))
        parser.add_argument(
            '--description',
            help=_('Description for the firewall rule'))
        parser.add_argument(
            '--protocol',
            help=_('IP Protocol. Integer should be [0:255]'))
        parser.add_argument(
            '--src-port-range',
            help=_('Range in a:b or integer in [1, 65535]'))
        parser.add_argument(
            '--dst-port-range',
            help=_('Range in a:b or integer in [1, 65535]'))
        parser.add_argument(
            '--source-ip-address',
            help=_('Source IP address'))
        parser.add_argument(
            '--destination-ip-address',
            help=_('Destination IP address'))

    def args2body(self, parsed_args):
        body = {self.resource: {}, }
        neutronv20.update_dict(parsed_args, body[self.resource],
                               ['name', 'description', 'protocol',
                                'src_port_range', 'dst_port_range',
                                'source_ip_address', 'destination_ip_address',
                                'tenant_id'])
        return body


class DeleteSteeringClassifier(neutronv20.DeleteCommand):
    """Delete a given classifier"""

    resource = 'steering_classifier'
    log = logging.getLogger(__name__ + '.DeleteSteeringClassifier')


class UpdateSteeringClassifier(neutronv20.UpdateCommand):
    """Update a given classifier"""

    resource = 'steering_classifier'
    log = logging.getLogger(__name__ + '.UpdateSteeringClassifier')
