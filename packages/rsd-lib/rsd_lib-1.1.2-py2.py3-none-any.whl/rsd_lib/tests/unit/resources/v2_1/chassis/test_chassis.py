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

import json
import mock

from sushy.tests.unit import base

from rsd_lib.resources.v2_1.chassis import chassis
from rsd_lib.resources.v2_1.chassis import power
from rsd_lib.resources.v2_1.chassis import power_zone
from rsd_lib.resources.v2_1.chassis import thermal
from rsd_lib.resources.v2_1.chassis import thermal_zone


class TestChassis(base.TestCase):
    def setUp(self):
        super(TestChassis, self).setUp()
        self.conn = mock.Mock()

        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/chassis.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.chassis_inst = chassis.Chassis(
            self.conn, "/redfish/v1/Chassis/chassis1", redfish_version="1.0.2"
        )

    def test_parse_attributes(self):
        self.assertEqual("1.0.2", self.chassis_inst.redfish_version)
        self.assertEqual("FlexChassis1", self.chassis_inst.asset_tag)
        self.assertEqual("RackMount", self.chassis_inst.chassis_type)
        self.assertEqual(
            "description-as-string", self.chassis_inst.description
        )
        self.assertEqual("1", self.chassis_inst.identity)
        self.assertEqual("Intel Corporation", self.chassis_inst.manufacturer)
        self.assertEqual("name-as-string", self.chassis_inst.name)
        self.assertEqual(
            "part-number-as-string", self.chassis_inst.part_number
        )
        self.assertEqual(
            "serial-number-as-string", self.chassis_inst.serial_number
        )
        self.assertEqual("sku-as-string", self.chassis_inst.sku)
        self.assertEqual("model-as-string", self.chassis_inst.model)
        self.assertEqual("Unknown", self.chassis_inst.indicator_led)
        self.assertEqual("Enabled", self.chassis_inst.status.state)
        self.assertEqual("OK", self.chassis_inst.status.health)
        self.assertEqual(None, self.chassis_inst.status.health_rollup)
        # chassis links section
        self.assertEqual(
            ("/redfish/v1/Chassis/Drawer1",), self.chassis_inst.links.contains
        )
        self.assertEqual(None, self.chassis_inst.links.contained_by)
        self.assertEqual(
            (
                "/redfish/v1/Systems/system1",
                "/redfish/v1/Systems/system2",
                "/redfish/v1/Systems/system3",
                "/redfish/v1/Systems/system4",
            ),
            self.chassis_inst.links.computer_systems,
        )
        self.assertEqual(
            ("/redfish/v1/Managers/RMM",), self.chassis_inst.links.managed_by
        )
        self.assertEqual(
            ("/redfish/v1/Managers/RMM",),
            self.chassis_inst.links.managers_in_chassis,
        )
        self.assertEqual(
            (), self.chassis_inst.links.oem.intel_rackscale.switches
        )
        # chassis oem section
        self.assertEqual(
            "Rack1", self.chassis_inst.oem.intel_rackscale.location.identity
        )
        self.assertEqual(
            "Pod1", self.chassis_inst.oem.intel_rackscale.location.parent_id
        )
        self.assertEqual(
            True, self.chassis_inst.oem.intel_rackscale.rmm_present
        )
        self.assertEqual(
            True,
            self.chassis_inst.oem.intel_rackscale.
            rack_supports_disaggregated_power_cooling
        )
        self.assertEqual(
            "Unique ID", self.chassis_inst.oem.intel_rackscale.uuid
        )
        self.assertEqual(
            "54.348103, 18.645172",
            self.chassis_inst.oem.intel_rackscale.geo_tag,
        )
        self.assertEqual("On", self.chassis_inst.power_state)
        self.assertEqual(
            1, self.chassis_inst.physical_security.intrusion_sensor_number
        )
        self.assertEqual(
            2, self.chassis_inst.physical_security.intrusion_sensor
        )
        self.assertEqual(
            3, self.chassis_inst.physical_security.intrusion_sensor_re_arm
        )
        self.assertEqual(
            ("/redfish/v1/Drives/1",), self.chassis_inst.links.drives
        )
        self.assertEqual(
            ("/redfish/v1/Storage/1",), self.chassis_inst.links.storage
        )
        self.assertEqual(
            ("/redfish/v1/Cool/1",), self.chassis_inst.links.cooled_by
        )
        self.assertEqual(
            ("/redfish/v1/Power/1",), self.chassis_inst.links.powered_by
        )

    def test_power_zones(self):
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/"
            "power_zone_collection.json",
            "r",
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_power_zones = self.chassis_inst.power_zones
        # | THEN |
        self.assertIsInstance(
            actual_power_zones, power_zone.PowerZoneCollection
        )
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_power_zones, self.chassis_inst.power_zones)
        self.conn.get.return_value.json.assert_not_called()

    def test_power_zones_on_refresh(self):
        # | GIVEN |
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/"
            "power_zone_collection.json",
            "r",
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(
            self.chassis_inst.power_zones, power_zone.PowerZoneCollection
        )

        # On refreshing the chassis instance...
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/chassis.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.chassis_inst.invalidate()
        self.chassis_inst.refresh(force=False)

        # | GIVEN |
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/"
            "power_zone_collection.json",
            "r",
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(
            self.chassis_inst.power_zones, power_zone.PowerZoneCollection
        )

    def test_power(self):
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open("rsd_lib/tests/unit/json_samples/v2_1/power.json", "r") as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_power = self.chassis_inst.power
        # | THEN |
        self.assertIsInstance(actual_power, power.Power)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_power, self.chassis_inst.power)
        self.conn.get.return_value.json.assert_not_called()

    def test_power_on_refresh(self):
        # | GIVEN |
        with open("rsd_lib/tests/unit/json_samples/v2_1/power.json", "r") as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.chassis_inst.power, power.Power)

        # On refreshing the chassis instance...
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/chassis.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.chassis_inst.invalidate()
        self.chassis_inst.refresh(force=False)

        # | GIVEN |
        with open("rsd_lib/tests/unit/json_samples/v2_1/power.json", "r") as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.chassis_inst.power, power.Power)

    def test_thermal_zones(self):
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/"
            "thermal_zone_collection.json",
            "r",
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_thermal_zones = self.chassis_inst.thermal_zones
        # | THEN |
        self.assertIsInstance(
            actual_thermal_zones, thermal_zone.ThermalZoneCollection
        )
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(actual_thermal_zones, self.chassis_inst.thermal_zones)
        self.conn.get.return_value.json.assert_not_called()

    def test_thermal_zones_on_refresh(self):
        # | GIVEN |
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/"
            "thermal_zone_collection.json",
            "r",
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(
            self.chassis_inst.thermal_zones, thermal_zone.ThermalZoneCollection
        )

        # On refreshing the chassis instance...
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/chassis.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.chassis_inst.invalidate()
        self.chassis_inst.refresh(force=False)

        # | GIVEN |
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/"
            "thermal_zone_collection.json",
            "r",
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(
            self.chassis_inst.thermal_zones, thermal_zone.ThermalZoneCollection
        )

    def test_thermal(self):
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/thermal.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_thermal = self.chassis_inst.thermal
        # | THEN |
        self.assertIsInstance(actual_thermal, thermal.Thermal)
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIsInstance(actual_thermal, thermal.Thermal)
        self.conn.get.return_value.json.assert_not_called()

    def test_thermal_on_refresh(self):
        # | GIVEN |
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/thermal.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.chassis_inst.thermal, thermal.Thermal)

        # On refreshing the chassis instance...
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/chassis.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.chassis_inst.invalidate()
        self.chassis_inst.refresh(force=False)

        # | GIVEN |
        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/thermal.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.chassis_inst.thermal, thermal.Thermal)

    def test_update(self):
        self.chassis_inst.update(asset_tag="Rack#1", location_id="1234")
        self.chassis_inst._conn.patch.assert_called_once_with(
            "/redfish/v1/Chassis/chassis1",
            data={
                "AssetTag": "Rack#1",
                "Oem": {"Intel_RackScale": {"Location": {"Id": "1234"}}},
            },
        )

        self.chassis_inst._conn.patch.reset_mock()
        self.chassis_inst.update(asset_tag="Rack#1")
        self.chassis_inst._conn.patch.assert_called_once_with(
            "/redfish/v1/Chassis/chassis1", data={"AssetTag": "Rack#1"}
        )

        self.chassis_inst._conn.patch.reset_mock()
        self.chassis_inst.update(location_id="1234")
        self.chassis_inst._conn.patch.assert_called_once_with(
            "/redfish/v1/Chassis/chassis1",
            data={"Oem": {"Intel_RackScale": {"Location": {"Id": "1234"}}}},
        )


class TestChassisCollection(base.TestCase):
    def setUp(self):
        super(TestChassisCollection, self).setUp()
        self.conn = mock.Mock()

        with open(
            "rsd_lib/tests/unit/json_samples/v2_1/" "chassis_collection.json",
            "r",
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.chassis_col = chassis.ChassisCollection(
            self.conn, "/redfish/v1/Systems", redfish_version="1.0.2"
        )

    def test__parse_attributes(self):
        self.assertEqual("1.0.2", self.chassis_col.redfish_version)
        self.assertEqual("Chassis Collection", self.chassis_col.name)
        self.assertIn(
            "/redfish/v1/Chassis/Chassis1", self.chassis_col.members_identities
        )

    @mock.patch.object(chassis, "Chassis", autospec=True)
    def test_get_member(self, mock_chassis):
        self.chassis_col.get_member("/redfish/v1/Chassis/Chassis1")

        mock_chassis.assert_called_once_with(
            self.chassis_col._conn,
            "/redfish/v1/Chassis/Chassis1",
            redfish_version=self.chassis_col.redfish_version,
            registries=None,
        )

    @mock.patch.object(chassis, "Chassis", autospec=True)
    def test_get_members(self, mock_chassis):
        members = self.chassis_col.get_members()
        self.assertEqual(mock_chassis.call_count, 8)
        self.assertIsInstance(members, list)
        self.assertEqual(8, len(members))
