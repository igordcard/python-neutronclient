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

from neutronclient.neutron.v2_0.ts import steering_classifier
from neutronclient.tests.unit import test_cli20


class CLITestV20ClassifierJSON(test_cli20.CLITestV20Base):

    def test_create_steering_classifier_with_all_params(self):
        resource = 'steering_classifier'
        cmd = steering_classifier.CreateSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                  None)
        name = 'myclassifier'
        my_id = 'myid'
        description = 'classifier description'
        type = 'unicast'
        protocol = '6'
        port_range = '5000:6000'
        src_ip = '1.1.1.1'
        dst_ip = '2.2.2.2'

        args = ['--name', name,
                '--description', description,
                '--type', type,
                '--protocol', protocol,
                '--port-range', port_range,
                '--source-ip-address', src_ip,
                '--destination-ip-address', dst_ip]
        position_names = ['name', 'description', 'type', 'protocol',
                          'port_range', 'source_ip_address',
                          'destination_ip_address']
        position_values = [name, description, type, protocol, port_range,
                           src_ip, dst_ip]
        self._test_create_resource(resource, cmd, name, my_id, args,
                                   position_names, position_values)

    def test_list_steering_classifiers(self):
        resources = 'steering_classifiers'
        cmd = steering_classifier.ListSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                None)
        self._test_list_resources(resources, cmd, True)

    def test_list_steering_classifiers_pagination(self):
        resources = 'steering_classifiers'
        cmd = steering_classifier.ListSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                         None)
        self._test_list_resources_with_pagination(resources, cmd)

    def test_list_steering_classifiers_sort(self):
        resources = 'steering_classifiers'
        cmd = steering_classifier.ListSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                None)
        self._test_list_resources(resources, cmd,
                                  sort_key=['name', 'id'],
                                  sort_dir=['asc', 'desc'])

    def test_list_steering_classifiers_limit(self):
        resources = 'steering_classifiers'
        cmd = steering_classifier.ListSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                None)
        self._test_list_resources(resources, cmd, page_size=1000)

    def test_show_steering_classifier_id(self):
        resource = 'steering_classifier'
        cmd = steering_classifier.ShowSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                None)
        args = ['--fields', 'id', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id, args, ['id'])

    def test_show_steering_classifier_id_name(self):
        resource = 'steering_classifier'
        cmd = steering_classifier.ShowSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                None)
        args = ['--fields', 'id', '--fields', 'name', self.test_id]
        self._test_show_resource(resource, cmd, self.test_id,
                                 args, ['id', 'name'])

    def test_update_steering_classifier(self):
        resource = 'steering_classifier'
        cmd = steering_classifier.UpdateSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                  None)
        self._test_update_resource(resource, cmd, 'myid',
                                   ['myid', '--name', 'myname',
                                    '--protocol', '1'],
                                   {'name': 'myname',
                                    'protocol': '1'})

    def test_delete_steering_classifier(self):
        resource = 'steering_classifier'
        cmd = steering_classifier.DeleteSteeringClassifier(test_cli20.MyApp(sys.stdout),
                                                  None)
        my_id = 'my-id'
        args = [my_id]
        self._test_delete_resource(resource, cmd, my_id, args)


class CLITestV20ClassifierXML(CLITestV20ClassifierJSON):
    format = 'xml'
