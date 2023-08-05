# Copyright 2018 Intel, Inc.
# All Rights Reserved.
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

from sushy.resources import base

from rsd_lib import exceptions as rsd_lib_exceptions
from rsd_lib.resources import v2_1
from rsd_lib.resources.v2_2.chassis import chassis
from rsd_lib.resources.v2_2.ethernet_switch import ethernet_switch
from rsd_lib.resources.v2_2.fabric import fabric
from rsd_lib.resources.v2_2.node import node
from rsd_lib.resources.v2_2.system import system
from rsd_lib.resources.v2_2.telemetry_service import telemetry_service
from rsd_lib.resources.v2_2.types import RESOURCE_CLASS
from rsd_lib.resources.v2_2.update_service import update_service


class RSDLibV2_2(v2_1.RSDLibV2_1):

    _ethernet_switches_path = base.Field(
        ["Oem", "Intel_RackScale", "EthernetSwitches", "@odata.id"]
    )
    """EthernetSwitchCollecton path"""

    _nodes_path = base.Field(
        ["Oem", "Intel_RackScale", "Nodes", "@odata.id"], required=True
    )
    """NodeCollection path"""

    _storage_service_path = base.Field(
        ["Oem", "Intel_RackScale", "Services", "@odata.id"]
    )
    """StorageServiceCollection path"""

    _telemetry_service_path = base.Field(["TelemetryService", "@odata.id"])
    """Telemetry Service path"""

    _update_service_path = base.Field(["UpdateService", "@odata.id"])
    """Update Service path"""

    def get_chassis_collection(self):
        """Get the ChassisCollection object

        :raises: MissingAttributeError, if the collection attribute is
            not found
        :returns: a ChassisCollection object
        """
        return chassis.ChassisCollection(
            self._conn,
            self._chassis_path,
            redfish_version=self.redfish_version,
        )

    def get_chassis(self, identity):
        """Given the identity return a Chassis object

        :param identity: The identity of the Chassis resource
        :returns: The Chassis object
        """
        return chassis.Chassis(
            self._conn, identity, redfish_version=self.redfish_version
        )

    def get_system(self, identity):
        """Given the identity return a System object

        :param identity: The identity of the System resource
        :returns: The System object
        """
        return system.System(
            self._conn, identity, redfish_version=self.redfish_version
        )

    def get_system_collection(self):
        """Get the SystemCollection object

        :raises: MissingAttributeError, if the collection attribute is
            not found
        :returns: a SystemCollection object
        """
        return system.SystemCollection(
            self._conn,
            self._systems_path,
            redfish_version=self.redfish_version,
        )

    def get_node_collection(self):
        """Get the NodeCollection object

        :raises: MissingAttributeError, if the collection attribute is
            not found
        :returns: a NodeCollection object
        """
        return node.NodeCollection(
            self._conn, self._nodes_path, redfish_version=self.redfish_version
        )

    def get_telemetry_service(self):
        """Given the identity return a Telemetry Service object

        :param identity: The identity of the Telemetry Service resource
        :returns: The Telemetry Service object
        """
        return telemetry_service.TelemetryService(
            self._conn,
            self._telemetry_service_path,
            redfish_version=self.redfish_version,
        )

    def get_ethernet_switch_collection(self):
        """Get the EthernetSwitchCollection object

        :raises: MissingAttributeError, if the collection attribute is
            not found
        :returns: a EthernetSwitchCollection object
        """
        return ethernet_switch.EthernetSwitchCollection(
            self._conn,
            self._ethernet_switches_path,
            redfish_version=self.redfish_version,
        )

    def get_ethernet_switch(self, identity):
        """Given the identity return a EthernetSwitch object

        :param identity: The identity of the EthernetSwitch resource
        :returns: The EthernetSwitch object
        """
        return ethernet_switch.EthernetSwitch(
            self._conn, identity, redfish_version=self.redfish_version
        )

    def get_update_service(self):
        """Get a UpdateService object

        :returns: The UpdateService object
        """
        return update_service.UpdateService(
            self._conn,
            self._update_service_path,
            redfish_version=self.redfish_version,
        )

    def get_fabric_collection(self):
        """Get the FabricCollection object

        :raises: MissingAttributeError, if the collection attribute is
            not found
        :returns: a FabricCollection object
        """
        return fabric.FabricCollection(
            self._conn,
            self._fabrics_path,
            redfish_version=self.redfish_version,
        )

    def get_fabric(self, identity):
        """Given the identity return a Fabric object

        :param identity: The identity of the Fabric resource
        :returns: The Fabric object
        """
        return fabric.Fabric(
            self._conn, identity, redfish_version=self.redfish_version
        )

    def get_resource(self, path):
        """Return corresponding resource object from path

        :param path: The path of a resource or resource collection
        :returns: corresponding resource or resource collection object
        """
        resource_class = self._get_resource_class_from_path(
            path,
            RESOURCE_CLASS)
        if not resource_class:
            raise rsd_lib_exceptions.NoMatchingResourceError(uri=path)
        return resource_class(
            self._conn, path, redfish_version=self.redfish_version
        )
