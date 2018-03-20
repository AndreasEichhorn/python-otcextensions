# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from openstack import resource

from otcextensions.sdk.auto_scaling import auto_scaling_service
from otcextensions.sdk import sdk_resource
from otcextensions.sdk.auto_scaling.v1 import _base


class InstanceConfig(sdk_resource.Resource):
    #: Properties
    #: reserved property
    #: Server Instance reference Id, if set, auto-scaling-group will create
    #: new instance use the same config as this one.
    instance_id = resource.Body('instance_id')
    #: reserved property
    instance_name = resource.Body('instance_name')
    #: The flavor reference to be used
    flavor_id = resource.Body('flavorRef')
    #: The image reference to be used
    image_id = resource.Body('imageRef')
    #: The disks to be used
    disk = resource.Body('disk', type=list)
    #: The SSH key used to login server instance
    key_name = resource.Body('key_name')
    #: When a server is first created, it provides the administrator password.
    admin_password = resource.Body('adminPass')
    #: The file path and contents, text only, to inject into the server at
    #: launch. The maximum size of the file path data is 255 bytes.
    #: The maximum limit is The number of allowed bytes in the decoded,
    #: rather than encoded, data.
    personality = resource.Body('personality')
    #: EIP config for creating new instance
    public_ip = resource.Body('public_ip')
    #: reserved property, not used for now
    user_data = resource.Body('user_data')
    #: Metadata(key-pair) for creating new instance
    metadata = resource.Body('metadata', type=dict)


class Config(_base.Resource):
    resource_key = 'scaling_configuration'
    resources_key = 'scaling_configurations'
    base_path = '/scaling_configuration'
    # query_marker_key = 'start_number'
    # service = auto_scaling_service.AutoScalingService()

    # capabilities
    allow_create = True
    allow_list = True
    allow_get = True
    allow_delete = True

    # _query_mapping = resource.QueryParameters(
    #     'marker', 'limit',
    #     # name='scaling_configuration_name',
    #     marker=query_marker_key,
    #     limit='limit'
    # )

    #: Properties
    #: AutoScaling config ID
    id = resource.Body('scaling_configuration_id', alternate_id=True)
    #: AutoScaling config name
    name = resource.Body('scaling_configuration_name')
    #: AutoScaling config created time
    create_time = resource.Body('create_time')
    #: AutoScaling config status
    status = resource.Body('status')
    #: Use the exists instance as template to create new instance
    instance_config = resource.Body('instance_config',
                                    # default={},
                                    type=InstanceConfig)

    def batch_delete(self, session, configs):
        '''batch delete auto-scaling configs

        make sure all configs should not been used by auto-scaling group
        :param session: openstack session
        :param list configs: The list item value can be the ID of a config
             or a :class:`~openstack.auto_scaling.v2.config.Config` instance.
        :return:
        '''
        ids = [config.id if isinstance(config, Config) else config
               for config in configs]
        json_body = {'scaling_configuration_id': ids}
        return session.post('/scaling_configurations',
                            headers={'Accept': '*'},
                            json=json_body)

    @classmethod
    def _get_next_link(cls, uri, response, data, marker, limit, total_yielded):
        next_link = None
        params = {}
        if total_yielded < data['total_number']:
            next_link = uri
            params['marker'] = total_yielded
            params['limit'] = limit
        else:
            next_link = None
        query_params = cls._query_mapping._transpose(params)
        return next_link, query_params
