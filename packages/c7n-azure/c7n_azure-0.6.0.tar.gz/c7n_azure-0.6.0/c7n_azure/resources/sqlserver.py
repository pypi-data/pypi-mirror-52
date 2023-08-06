# Copyright 2018 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from c7n_azure.filters import FirewallRulesFilter, FirewallBypassFilter
from c7n_azure.provider import resources
from c7n_azure.resources.arm import ArmResourceManager
from netaddr import IPRange, IPSet


@resources.register('sqlserver')
class SqlServer(ArmResourceManager):
    """SQL Server Resource

    :example:

    This policy will find all SQL servers with average DTU consumption under
    10 percent over the last 72 hours

    .. code-block:: yaml

        policies:
          - name: sqlserver-under-utilized
            resource: azure.sqlserver
            filters:
              - type: metric
                metric: dtu_consumption_percent
                op: lt
                aggregation: average
                threshold: 10
                timeframe: 72
                filter: "ElasticPoolResourceId eq '*'"
                no_data_action: include

    :example:

    This policy will find all SQL servers without any firewall rules defined.

    .. code-block:: yaml

        policies:
          - name: find-sqlserver-without-firewall-rules
            resource: azure.sqlserver
            filters:
              - type: firewall-rules
                equal: []

    :example:

    This policy will find all SQL servers allowing traffic from 1.2.2.128/25 CIDR.

    .. code-block:: yaml

        policies:
          - name: find-sqlserver-allowing-subnet
            resource: azure.sqlserver
            filters:
              - type: firewall-rules
                include: ['1.2.2.128/25']
    """

    class resource_type(ArmResourceManager.resource_type):
        doc_groups = ['Databases']

        service = 'azure.mgmt.sql'
        client = 'SqlManagementClient'
        enum_spec = ('servers', 'list', None)
        resource_type = 'Microsoft.Sql/servers'


@SqlServer.filter_registry.register('firewall-rules')
class SqlServerFirewallRulesFilter(FirewallRulesFilter):
    def _query_rules(self, resource):
        query = self.client.firewall_rules.list_by_server(
            resource['resourceGroup'],
            resource['name'])

        resource_rules = IPSet()

        for r in query:
            if r.start_ip_address == '0.0.0.0' and r.end_ip_address == '0.0.0.0':
                # Ignore 0.0.0.0 magic value representing Azure Cloud bypass
                continue
            resource_rules.add(IPRange(r.start_ip_address, r.end_ip_address))

        return resource_rules


@SqlServer.filter_registry.register('firewall-bypass')
class SqlServerFirewallBypassFilter(FirewallBypassFilter):
    """
    Filters resources by the firewall bypass rules.

    :example:

    This policy will find all SQL Servers with enabled Azure Services bypass rules

    .. code-block:: yaml

        policies:
          - name: sqlserver-bypass
            resource: azure.sqlserver
            filters:
              - type: firewall-bypass
                mode: equal
                list:
                    - AzureServices
    """

    schema = FirewallBypassFilter.schema(['AzureServices'])

    def _query_bypass(self, resource):
        # Remove spaces from the string for the comparision
        query = self.client.firewall_rules.list_by_server(
            resource['resourceGroup'],
            resource['name'])

        for r in query:
            if r.start_ip_address == '0.0.0.0' and r.end_ip_address == '0.0.0.0':
                return ['AzureServices']
        return []
