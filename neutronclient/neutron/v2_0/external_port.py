# Copyright (c) 2014 Igor Duarte Cardoso.
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
#
# @author: Igor Duarte Cardoso

import logging

from neutronclient.neutron import v2_0 as neutronV20
from neutronclient.openstack.common.gettextutils import _


class CreateAttachmentPoint(neutronV20.CreateCommand):
    """Create a new attachment point."""

    resource = 'attachment_point'
    log = logging.getLogger(__name__ + '.CreateAttachmentPoint')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            help='name of this attachment point')
        parser.add_argument(
            '--description',
            help='a long description name of this attachment point')
        parser.add_argument(
            '--network_id',
            help='ID of the network to be attached to this attachment point')
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state',
            action='store_false',
            help='set admin state up to false')
        parser.add_argument(
            'ip_address',
            metavar='IP_ADDRESS',
            help='IP address used to reach the attachment point')
        parser.add_argument(
            'driver',
            metavar='DRIVER',
            help='name of the driver responsible for communicating with this attachment point')
        parser.add_argument(
            'identifier',
            metavar='IDENTIFIER',
            help='identifier of the attachment point based on the specified driver')
        parser.add_argument(
            'technology',
            metavar='TECHNOLOGY',
            help='technology to be used by this attachment point, in order for OpenStack to agree with it (e.g. gre).')

    def args2body(self, parsed_args):
        body = {'attachment_point': {'ip_address': parsed_args.ip_address,
                                  'driver': parsed_args.driver,
                                  'identifier': parsed_args.identifier,
                                  'technology': parsed_args.technology,
                                  'admin_state_up': parsed_args.admin_state}}

        if parsed_args.name:
            body['attachment_point'].update({'name': parsed_args.name})
        if parsed_args.description:
            body['attachment_point'].update({'description': parsed_args.description})
        if parsed_args.tenant_id:
            body['attachment_point'].update({'tenant_id': parsed_args.tenant_id})
        if parsed_args.network_id:
            network_id = neutronV20.find_resourceid_by_name_or_id(
                self.get_client(), 'network', parsed_args.network_id)
            body['attachment_point'].update({'network_id': network_id})

        return body

class ShowAttachmentPoint(neutronV20.ShowCommand):
    """Show information of a given attachment point."""

    resource = 'attachment_point'
    log = logging.getLogger(__name__ + '.ShowAttachmentPoint')

class ListAttachmentPoint(neutronV20.ListCommand):
    """List attachment points that belong to a given tenant."""

    resource = 'attachment_point'
    log = logging.getLogger(__name__ + '.ListAttachmentPoint')
    list_columns = ['id', 'name', 'ip_address', 'driver', 'identifier', 'technology', 'network_id', 'status']

class UpdateAttachmentPoint(neutronV20.UpdateCommand):
    """Update a given attachment point."""

    resource = 'attachment_point'
    log = logging.getLogger(__name__ + '.UpdateAttachmentPoint')

class DeleteAttachmentPoint(neutronV20.DeleteCommand):
    """Delete a given attachment point."""

    resource = 'attachment_point'
    log = logging.getLogger(__name__ + '.DeleteAttachmentPoint')

class AttachAttachmentPoint(neutronV20.NeutronCommand):
    """Attach an attachment point to a given network."""

    api = 'network'
    resource = 'attachment_point '
    log = logging.getLogger(__name__ + '.AttachAttachmentPoint')

    def get_parser(self, prog_name):
        parser = super(AttachAttachmentPoint, self).get_parser(prog_name)
        parser.add_argument(
            'attachment_point', metavar='ATTACHMENT_POINT',
            help='ID or name of the attachment point')
        parser.add_argument(
            'network_id', metavar='NETWORK',
            help='ID or name of the network to attach this attachment point')
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format

        ap_id = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'attachment_point', parsed_args.attachment_point)
        network_id = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'network', parsed_args.network_id)

        body = {'attachment_point': {}}
        body['attachment_point'].update({'network_id': network_id})

        neutron_client.update_attachment_point(ap_id, body)

        print >>self.app.stdout, (
            _('Attachment point %s attached to network %s') %
            (parsed_args.attachment_point, parsed_args.network_id))

class DetachAttachmentPoint(neutronV20.NeutronCommand):
    """Detach an attachment point from a network."""

    api = 'network'
    resource = 'attachment_point '
    log = logging.getLogger(__name__ + '.DetachAttachmentPoint')

    def get_parser(self, prog_name):
        parser = super(DetachAttachmentPoint, self).get_parser(prog_name)
        parser.add_argument(
            'attachment_point', metavar='ATTACHMENT_POINT',
            help='ID or name of the attachment point')
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format

        ap_id = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'attachment_point', parsed_args.attachment_point)

        body = {'attachment_point': {}}
        body['attachment_point'].update({'network_id': None})

        neutron_client.update_attachment_point(ap_id, body)

        print >>self.app.stdout, (
            _('Attachment point %s detached from network') % (
                parsed_args.attachment_point))

class CreateExternalPort(neutronV20.CreateCommand):
    """Request the creation of an external port on a given attachment point."""

    resource = 'external_port'
    log = logging.getLogger(__name__ + '.CreateExternalPort')

    def add_known_arguments(self, parser):
        parser.add_argument(
            '--name',
            help='name of this external port')
        parser.add_argument(
            '--description',
            help='a long description name of this external port')
        parser.add_argument(
            '--port_id',
            help='ID of the neutron port to be attached to this external port')
        parser.add_argument(
            '--admin-state-down',
            dest='admin_state',
            action='store_false',
            help='set admin state up to false')
        parser.add_argument(
            'mac_address',
            metavar='MAC_ADDRESS',
            help='MAC address used to reach the endpoint of this external port')
        parser.add_argument(
            'attachment_point_id',
            metavar='ATTACHMENT_POINT',
            help='ID or name of the attachment point used to reach the endpoint of this external port')

    def args2body(self, parsed_args):
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format
        attachment_point_id = neutronV20.find_resourceid_by_name_or_id(neutron_client, 'attachment_point', parsed_args.attachment_point_id)

        body = {'external_port': {'mac_address': parsed_args.mac_address,
                                  'attachment_point_id': attachment_point_id,
                                  'admin_state_up': parsed_args.admin_state}}

        if parsed_args.name:
            body['external_port'].update({'name': parsed_args.name})
        if parsed_args.description:
            body['external_port'].update({'description': parsed_args.description})
        if parsed_args.tenant_id:
            body['attachment_point'].update({'tenant_id': parsed_args.tenant_id})
        if parsed_args.description:
            body['external_port'].update({'port_id': parsed_args.port_id})


        return body

class ShowExternalPort(neutronV20.ShowCommand):
    """Show information of a given external port."""

    resource = 'external_port'
    log = logging.getLogger(__name__ + '.ShowExternalPort')

class ListExternalPort(neutronV20.ListCommand):
    """List external ports that belong to a given attachment point."""

    resource = 'external_port'
    log = logging.getLogger(__name__ + '.ListExternalPort')
    list_columns = ['id', 'name', 'mac_address', 'attachment_point_id', 'port_id', 'status']

class UpdateExternalPort(neutronV20.UpdateCommand):
    """Update a given external port."""

    resource = 'external_port'
    log = logging.getLogger(__name__ + '.UpdateExternalPort')

class DeleteExternalPort(neutronV20.DeleteCommand):
    """Delete a given external port."""

    resource = 'external_port'
    log = logging.getLogger(__name__ + '.DeleteExternalPort')

class AttachExternalPort(neutronV20.NeutronCommand):
    """Attach an external port to _the_ network, creating a port during the process."""

    resource = 'external_port '
    log = logging.getLogger(__name__ + '.AttachExternalPort')

    def get_parser(self, prog_name):
        parser = super(AttachExternalPort, self).get_parser(prog_name)
        parser.add_argument(
            'external_port', metavar='EXTERNAL_PORT',
            help='ID or name of the external port')
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format

        eport_id = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'external_port', parsed_args.external_port)

        body = {'external_port': {}}

        data = neutron_client.update_external_port(eport_id, body)

        self.format_output_data(data)

        port_id = data['external_port']['port_id']

        print >>self.app.stdout, (
            _('%s') %
            (port_id))

# TODO: Not currently working.
class DetachExternalPort(neutronV20.NeutronCommand):
    """Detach an external port from a port."""

    resource = 'external_port '
    log = logging.getLogger(__name__ + '.DetachExternalPort')

    def get_parser(self, prog_name):
        parser = super(DetachExternalPort, self).get_parser(prog_name)
        parser.add_argument(
            'external_port', metavar='EXTERNAL_PORT',
            help='ID or name of the external port')
        return parser

    def run(self, parsed_args):
        self.log.debug('run(%s)' % parsed_args)
        neutron_client = self.get_client()
        neutron_client.format = parsed_args.request_format

        eport_id = neutronV20.find_resourceid_by_name_or_id(
            neutron_client, 'external_port', parsed_args.external_port)

        body = {'external_port': {}}
        body['external_port'].update({'port_id': None})

        neutron_client.update_external_port(eport_id, body)

        print >>self.app.stdout, (
            _('External port %s detached from port') % (
                parsed_args.external_port))
