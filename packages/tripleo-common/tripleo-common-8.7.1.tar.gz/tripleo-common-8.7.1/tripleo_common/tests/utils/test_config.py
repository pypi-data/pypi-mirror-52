#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import datetime
import fixtures
import mock
import os
import uuid
import warnings
import yaml

from mock import call
from mock import patch

from tripleo_common import constants
from tripleo_common.tests import base
from tripleo_common.tests.fake_config import fakes
from tripleo_common.utils import config as ooo_config


class TestConfig(base.TestCase):

    def setUp(self):
        super(TestConfig, self).setUp()

    @patch.object(ooo_config.shutil, 'copyfile')
    @patch.object(ooo_config.Config, '_mkdir')
    @patch.object(ooo_config.Config, '_open_file')
    @mock.patch('tempfile.mkdtemp', autospec=True)
    def test_overcloud_config_generate_config(self,
                                              mock_tmpdir,
                                              mock_open,
                                              mock_mkdir,
                                              mock_copyfile):
        config_type_list = ['config_settings', 'global_config_settings',
                            'logging_sources', 'monitoring_subscriptions',
                            'service_config_settings',
                            'service_metadata_settings',
                            'service_names',
                            'upgrade_batch_tasks', 'upgrade_tasks',
                            'external_deploy_tasks']
        fake_role = [role for role in
                     fakes.FAKE_STACK['outputs'][1]['output_value']]

        heat = mock.MagicMock()
        heat.stacks.get.return_value = fakes.create_tht_stack()
        self.config = ooo_config.Config(heat)
        mock_tmpdir.return_value = "/tmp/tht"
        self.config.download_config('overcloud', '/tmp', config_type_list)

        expected_mkdir_calls = [call('/tmp/tht/%s' % r) for r in fake_role]
        mock_mkdir.assert_has_calls(expected_mkdir_calls, any_order=True)
        expected_calls = []
        for config in config_type_list:
            for role in fake_role:
                if 'external' in config:
                    continue
                elif config == 'step_config':
                    expected_calls += [call('/tmp/tht/%s/%s.pp' %
                                            (role, config))]
                else:
                    expected_calls += [call('/tmp/tht/%s/%s.yaml' %
                                            (role, config))]
        mock_open.assert_has_calls(expected_calls, any_order=True)

    @patch.object(ooo_config.shutil, 'copyfile')
    @patch.object(ooo_config.Config, '_mkdir')
    @patch.object(ooo_config.Config, '_open_file')
    @mock.patch('tempfile.mkdtemp', autospec=True)
    def test_overcloud_config_one_config_type(self,
                                              mock_tmpdir,
                                              mock_open,
                                              mock_mkdir,
                                              mock_copyfile):

        expected_config_type = 'config_settings'
        fake_role = [role for role in
                     fakes.FAKE_STACK['outputs'][1]['output_value']]

        heat = mock.MagicMock()
        heat.stacks.get.return_value = fakes.create_tht_stack()
        self.config = ooo_config.Config(heat)
        mock_tmpdir.return_value = "/tmp/tht"
        self.config.download_config('overcloud', '/tmp', ['config_settings'])
        expected_mkdir_calls = [call('/tmp/tht/%s' % r) for r in fake_role]
        expected_calls = [call('/tmp/tht/%s/%s.yaml'
                          % (r, expected_config_type))
                          for r in fake_role]
        mock_mkdir.assert_has_calls(expected_mkdir_calls, any_order=True)
        mock_open.assert_has_calls(expected_calls, any_order=True)

    @mock.patch('os.mkdir')
    @mock.patch('six.moves.builtins.open')
    @mock.patch('tempfile.mkdtemp', autospec=True)
    def test_overcloud_config_wrong_config_type(self, mock_tmpdir,
                                                mock_open, mock_mkdir):
        args = {'name': 'overcloud', 'config_dir': '/tmp',
                'config_type': ['bad_config']}
        heat = mock.MagicMock()
        heat.stacks.get.return_value = fakes.create_tht_stack()
        self.config = ooo_config.Config(heat)
        mock_tmpdir.return_value = "/tmp/tht"
        self.assertRaises(
            KeyError,
            self.config.download_config, *args)

    def test_overcloud_config_upgrade_tasks(self):

        heat = mock.MagicMock()
        heat.stacks.get.return_value = fakes.create_tht_stack()
        self.config = ooo_config.Config(heat)
        self.tmp_dir = self.useFixture(fixtures.TempDir()).path
        fake_role = [role for role in
                     fakes.FAKE_STACK['outputs'][1]['output_value']]
        expected_tasks = {'FakeController': [{'name': 'Stop fake service',
                                              'service': 'name=fake '
                                              'state=stopped',
                                              'when': 'step|int == 1'}],
                          'FakeCompute': [{'name': 'Stop fake service',
                                           'service':
                                           'name=fake state=stopped',
                                           'when': ['nova_api_enabled.rc == 0',
                                                    'httpd_enabled.rc != 0',
                                                    'step|int == 1']},
                                          {'name': 'Stop nova-'
                                           'compute service',
                                           'service':
                                           'name=openstack-nova-'
                                           'compute state=stopped',
                                           'when': [
                                               'nova_compute_enabled.rc == 0',
                                               'step|int == 2', 'existing',
                                               'list']}]}
        for role in fake_role:
            filedir = os.path.join(self.tmp_dir, role)
            os.makedirs(filedir)
            filepath = os.path.join(filedir, "upgrade_tasks_playbook.yaml")
            playbook_tasks = self.config._write_playbook_get_tasks(
                fakes.FAKE_STACK['outputs'][1]['output_value'][role]
                ['upgrade_tasks'], role, filepath)
            self.assertTrue(os.path.isfile(filepath))
            self.assertEqual(expected_tasks[role], playbook_tasks)

    def test_get_server_names(self):
        heat = mock.MagicMock()
        self.config = ooo_config.Config(heat)
        self.config.stack_outputs = {
            'RoleNetHostnameMap': {
                'Controller': {
                    'ctlplane': [
                        'c0.ctlplane.localdomain',
                        'c1.ctlplane.localdomain',
                        'c2.ctlplane.localdomain']}},
            'ServerIdData': {
                'server_ids': {
                    'Controller': [
                        '8269f736',
                        '2af0a373',
                        'c8479674']}}}
        server_names = self.config.get_server_names()
        expected = {'2af0a373': 'c1', '8269f736': 'c0', 'c8479674': 'c2'}
        self.assertEqual(expected, server_names)

    def test_get_role_config(self):
        heat = mock.MagicMock()
        self.config = ooo_config.Config(heat)
        self.config.stack_outputs = {'RoleConfig': None}
        role_config = self.config.get_role_config()
        self.assertEqual({}, role_config)

    def test_get_deployment_data(self):
        heat = mock.MagicMock()
        self.config = ooo_config.Config(heat)
        stack = 'overcloud'
        first = mock.MagicMock()
        first.creation_time = datetime.datetime.now() - datetime.timedelta(2)
        second = mock.MagicMock()
        second.creation_time = datetime.datetime.now() - datetime.timedelta(1)
        third = mock.MagicMock()
        third.creation_time = datetime.datetime.now()
        # Set return_value in a nonsorted order, as we expect the function to
        # sort, so that's what we want to test
        heat.resources.list.return_value = [second, third, first]

        deployment_data = self.config.get_deployment_data(stack)
        self.assertTrue(heat.resources.list.called)
        self.assertEqual(
            heat.resources.list.call_args,
            mock.call(stack,
                      filters=dict(name=constants.TRIPLEO_DEPLOYMENT_RESOURCE),
                      nested_depth=constants.NESTED_DEPTH,
                      with_detail=True))
        self.assertEqual(deployment_data,
                         [first, second, third])

    def _get_config_data(self, datafile):
        config_data_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            datafile)
        config_data = yaml.safe_load(open(config_data_path).read())
        deployment_data = []

        for deployment in config_data['deployments']:
            deployment_mock = mock.MagicMock()
            deployment_mock.id = deployment['deployment']
            deployment_mock.attributes = dict(
                value=dict(server=deployment['server'],
                           deployment=deployment['deployment'],
                           config=deployment['config'],
                           name=deployment['name']))
            deployment_data.append(deployment_mock)

        configs = config_data['configs']

        return deployment_data, configs

    def _get_config_dict(self, deployment):
        config = self.configs[deployment.attributes['value']['config']].copy()
        config['inputs'] = []
        config['inputs'].append(dict(
            name='deploy_server_id',
            value=deployment.attributes['value']['server']))
        return config

    def _get_yaml_file(self, file_name):
        file_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'data',
            file_name)
        return yaml.safe_load(open(file_path).read())

    @patch('tripleo_common.utils.config.Config.get_config_dict')
    @patch('tripleo_common.utils.config.Config.get_deployment_data')
    def test_config_download(self, mock_deployment_data, mock_config_dict):
        heat = mock.MagicMock()
        self.config = ooo_config.Config(heat)
        stack = mock.MagicMock()
        heat.stacks.get.return_value = stack

        stack.outputs = [
            {'output_key': 'RoleNetHostnameMap',
             'output_value': {
                 'Controller': {
                     'ctlplane': [
                         'overcloud-controller-0.ctlplane.localdomain']},
                 'Compute': {
                     'ctlplane': [
                         'overcloud-novacompute-0.ctlplane.localdomain',
                         'overcloud-novacompute-1.ctlplane.localdomain',
                         'overcloud-novacompute-2.ctlplane.localdomain']}}},
            {'output_key': 'ServerIdData',
             'output_value': {
                 'server_ids': {
                     'Controller': [
                         '00b3a5e1-5e8e-4b55-878b-2fa2271f15ad'],
                     'Compute': [
                         'a7db3010-a51f-4ae0-a791-2364d629d20d',
                         '8b07cd31-3083-4b88-a433-955f72039e2c',
                         '169b46f8-1965-4d90-a7de-f36fb4a830fe']}}}]
        deployment_data, configs = \
            self._get_config_data('config_data.yaml')
        self.configs = configs

        mock_deployment_data.return_value = deployment_data
        mock_config_dict.side_effect = self._get_config_dict

        self.tmp_dir = self.useFixture(fixtures.TempDir()).path
        tmp_path = self.config.download_config(stack, self.tmp_dir)

        for f in ['Controller',
                  'Compute', ]:

            self.assertEqual(
                yaml.safe_load(
                    open(os.path.join(tmp_path, 'group_vars', f)).read()),
                self._get_yaml_file(f))

        for d in ['ControllerHostEntryDeployment',
                  'NetworkDeployment',
                  'MyExtraConfigPost',
                  'MyPostConfig']:
            self.assertEqual(
                yaml.safe_load(
                    open(os.path.join(tmp_path, 'Controller',
                                      'overcloud-controller-0',
                                      d)).read()),
                self._get_yaml_file(os.path.join(
                                    'overcloud-controller-0',
                                    d)))

        for d in ['ComputeHostEntryDeployment',
                  'NetworkDeployment',
                  'MyExtraConfigPost']:
            self.assertEqual(
                yaml.safe_load(
                    open(os.path.join(tmp_path, 'Compute',
                                      'overcloud-novacompute-0',
                                      d)).read()),
                self._get_yaml_file(os.path.join(
                                    'overcloud-novacompute-0',
                                    d)))

        for d in ['ComputeHostEntryDeployment',
                  'NetworkDeployment',
                  'MyExtraConfigPost']:
            self.assertEqual(
                yaml.safe_load(
                    open(os.path.join(tmp_path, 'Compute',
                                      'overcloud-novacompute-1',
                                      d)).read()),
                self._get_yaml_file(os.path.join(
                                    'overcloud-novacompute-1',
                                    d)))

        for d in ['ComputeHostEntryDeployment',
                  'NetworkDeployment',
                  'MyExtraConfigPost',
                  'AnsibleDeployment']:
            self.assertEqual(
                yaml.safe_load(
                    open(os.path.join(tmp_path, 'Compute',
                                      'overcloud-novacompute-2',
                                      d)).read()),
                self._get_yaml_file(os.path.join(
                                    'overcloud-novacompute-2',
                                    d)))

    @patch('tripleo_common.utils.config.Config.get_config_dict')
    @patch('tripleo_common.utils.config.Config.get_deployment_data')
    def test_config_download_os_apply_config(
        self, mock_deployment_data, mock_config_dict):
        heat = mock.MagicMock()
        self.config = ooo_config.Config(heat)
        stack = mock.MagicMock()
        heat.stacks.get.return_value = stack

        stack.outputs = [
            {'output_key': 'RoleNetHostnameMap',
             'output_value': {
                 'Controller': {
                     'ctlplane': [
                         'overcloud-controller-0.ctlplane.localdomain']},
                 'Compute': {
                     'ctlplane': [
                         'overcloud-novacompute-0.ctlplane.localdomain',
                         'overcloud-novacompute-1.ctlplane.localdomain',
                         'overcloud-novacompute-2.ctlplane.localdomain']}}},
            {'output_key': 'ServerIdData',
             'output_value': {
                 'server_ids': {
                     'Controller': [
                         '00b3a5e1-5e8e-4b55-878b-2fa2271f15ad'],
                     'Compute': [
                         'a7db3010-a51f-4ae0-a791-2364d629d20d',
                         '8b07cd31-3083-4b88-a433-955f72039e2c',
                         '169b46f8-1965-4d90-a7de-f36fb4a830fe']}}}]
        deployment_data, configs = \
            self._get_config_data('config_data.yaml')

        # Add a group:os-apply-config config and deployment
        config_uuid = str(uuid.uuid4())
        configs[config_uuid] = dict(
            id=config_uuid,
            config=dict(a='a'),
            group='os-apply-config',
            outputs=[])

        deployment_uuid = str(uuid.uuid4())
        deployment_mock = mock.MagicMock()
        deployment_mock.id = deployment_uuid
        deployment_mock.attributes = dict(
            value=dict(server='00b3a5e1-5e8e-4b55-878b-2fa2271f15ad',
                       deployment=deployment_uuid,
                       config=config_uuid,
                       name='OsApplyConfigDeployment'))
        deployment_data.append(deployment_mock)

        self.configs = configs

        mock_deployment_data.return_value = deployment_data
        mock_config_dict.side_effect = self._get_config_dict

        self.tmp_dir = self.useFixture(fixtures.TempDir()).path
        with warnings.catch_warnings(record=True) as w:
            self.config.download_config(stack, self.tmp_dir)
            self.assertEqual(1, len(w))
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "group:os-apply-config is deprecated" in str(w[-1].message)

    @patch('tripleo_common.utils.config.Config.get_config_dict')
    @patch('tripleo_common.utils.config.Config.get_deployment_data')
    def test_config_download_no_deployment_uuid(self, mock_deployment_data,
                                                mock_config_dict):
        heat = mock.MagicMock()
        self.config = ooo_config.Config(heat)
        stack = mock.MagicMock()
        heat.stacks.get.return_value = stack
        stack.outputs = [
            {'output_key': 'RoleNetHostnameMap',
             'output_value': {
                 'Controller': {
                     'ctlplane': [
                         'overcloud-controller-0.ctlplane.localdomain']},
                 'Compute': {
                     'ctlplane': [
                         'overcloud-novacompute-0.ctlplane.localdomain',
                         'overcloud-novacompute-1.ctlplane.localdomain',
                         'overcloud-novacompute-2.ctlplane.localdomain']}}},
            {'output_key': 'ServerIdData',
             'output_value': {
                 'server_ids': {
                     'Controller': [
                         '00b3a5e1-5e8e-4b55-878b-2fa2271f15ad'],
                     'Compute': [
                         'a7db3010-a51f-4ae0-a791-2364d629d20d',
                         '8b07cd31-3083-4b88-a433-955f72039e2c',
                         '169b46f8-1965-4d90-a7de-f36fb4a830fe']}}},
            {'output_key': 'RoleGroupVars',
             'output_value': {
                 'Controller': {
                     'any_errors_fatal': 'yes',
                     'max_fail_percentage': 15},
                 'Compute': {
                     'any_errors_fatal': 'yes',
                     'max_fail_percentage': 15},
             }}]
        deployment_data, configs = self._get_config_data('config_data.yaml')

        # Set the deployment to TripleOSoftwareDeployment for the first
        # deployment
        deployment_data[0].attributes['value']['deployment'] = \
            'TripleOSoftwareDeployment'

        self.configs = configs
        mock_deployment_data.return_value = deployment_data
        mock_config_dict.side_effect = self._get_config_dict

        self.tmp_dir = self.useFixture(fixtures.TempDir()).path
        with warnings.catch_warnings(record=True) as w:
            self.config.download_config(stack, self.tmp_dir)
            assert "Skipping deployment" in str(w[-1].message)
