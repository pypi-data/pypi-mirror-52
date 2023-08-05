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

import json
import mock
import testtools

from sushy import exceptions

from rsd_lib.resources.v2_4.storage_service import capacity_source
from rsd_lib.resources.v2_4.storage_service import volume


class StorageServiceTestCase(testtools.TestCase):
    def setUp(self):
        super(StorageServiceTestCase, self).setUp()
        self.conn = mock.Mock()
        with open(
            "rsd_lib/tests/unit/json_samples/v2_4/volume.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.volume_inst = volume.Volume(
            self.conn,
            "/redfish/v1/StorageServices/NVMeoE1/Volumes/1",
            redfish_version="1.0.2",
        )

    def test__parse_attributes(self):
        self.assertEqual("1.0.2", self.volume_inst.redfish_version)
        self.assertEqual("Volume description", self.volume_inst.description)
        self.assertEqual("1", self.volume_inst.identity)
        self.assertEqual("NVMe remote storage", self.volume_inst.name)
        self.assertEqual("Enabled", self.volume_inst.status.state)
        self.assertEqual("OK", self.volume_inst.status.health)
        self.assertEqual("OK", self.volume_inst.status.health_rollup)
        self.assertIsNone(self.volume_inst.model)
        self.assertIsNone(self.volume_inst.manufacturer)
        self.assertEqual(
            ["Read", "Write"], self.volume_inst.access_capabilities
        )
        self.assertEqual(3071983104, self.volume_inst.capacity_bytes)
        self.assertEqual(3071983104, self.volume_inst.allocated_Bytes)
        self.assertEqual(
            "/dev/nvme1n1p1", self.volume_inst.identifiers[0].durable_name
        )
        self.assertEqual(
            "SystemPath", self.volume_inst.identifiers[0].durable_name_format
        )
        self.assertEqual(
            "iqn.2001-04.com.example:diskarrays-sn-a8675309",
            self.volume_inst.identifiers[1].durable_name,
        )
        self.assertEqual(
            "iQN", self.volume_inst.identifiers[1].durable_name_format
        )
        self.assertEqual(
            ("/redfish/v1/Fabrics/NVMeoE/Endpoints/1",),
            self.volume_inst.links.endpoints,
        )
        self.assertEqual(
            "/redfish/v1/StorageServices/NVMeoE1/Volumes/1/Metrics",
            self.volume_inst.links.metrics,
        )
        self.assertEqual(
            "SourceElement",
            self.volume_inst.replica_infos[0].replica_readonly_access,
        )
        self.assertEqual(
            "Snapshot", self.volume_inst.replica_infos[0].replica_type
        )
        self.assertEqual(
            "Target", self.volume_inst.replica_infos[0].replica_role
        )
        self.assertEqual(
            "/redfish/v1/StorageServices/NVMeoE1/Volumes/2",
            self.volume_inst.replica_infos[0].replica,
        )
        self.assertEqual(False, self.volume_inst.bootable)
        self.assertIsNone(self.volume_inst.erased)
        self.assertEqual(True, self.volume_inst.erase_on_detach)

    def test_capacity_sources(self):
        # | GIVEN |
        self.conn.get.return_value.json.reset_mock()
        with open(
            "rsd_lib/tests/unit/json_samples/v2_4/capacity_sources.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN |
        actual_capacity_sources = self.volume_inst.capacity_sources
        # | THEN |
        self.assertIsInstance(actual_capacity_sources, list)
        self.assertIsInstance(
            actual_capacity_sources[0], capacity_source.CapacitySource
        )
        self.conn.get.return_value.json.assert_called_once_with()

        # reset mock
        self.conn.get.return_value.json.reset_mock()
        # | WHEN & THEN |
        # tests for same object on invoking subsequently
        self.assertIs(
            actual_capacity_sources, self.volume_inst.capacity_sources
        )
        self.conn.get.return_value.json.assert_not_called()

    def test_capacity_sources_on_refresh(self):
        # | GIVEN |
        with open(
            "rsd_lib/tests/unit/json_samples/v2_4/capacity_sources.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.volume_inst.capacity_sources, list)
        self.assertIsInstance(
            self.volume_inst.capacity_sources[0],
            capacity_source.CapacitySource,
        )

        # On refreshing the telemetry service instance...
        with open(
            "rsd_lib/tests/unit/json_samples/v2_4/volume.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.volume_inst.invalidate()
        self.volume_inst.refresh(force=False)

        # | GIVEN |
        with open(
            "rsd_lib/tests/unit/json_samples/v2_4/capacity_sources.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())
        # | WHEN & THEN |
        self.assertIsInstance(self.volume_inst.capacity_sources, list)
        self.assertIsInstance(
            self.volume_inst.capacity_sources[0],
            capacity_source.CapacitySource,
        )

    def test_resize_volume(self):
        self.volume_inst.resize(3071983105)
        self.volume_inst._conn.patch.assert_called_once_with(
            "/redfish/v1/StorageServices/NVMeoE1/Volumes/1",
            data={"Capacity": {"Data": {"AllocatedBytes": 3071983105}}},
        )

    def test_update_volume_with_invalid_parameter(self):
        with self.assertRaisesRegex(
            exceptions.InvalidParameterValueError,
            'The parameter "num_bytes" value "fake-value" is invalid',
        ):
            self.volume_inst.resize("fake-value")

        with self.assertRaisesRegex(
            exceptions.InvalidParameterValueError,
            'The parameter "num_bytes" value "1024" is invalid',
        ):
            self.volume_inst.resize(1024)


class VolumeCollectionTestCase(testtools.TestCase):
    def setUp(self):
        super(VolumeCollectionTestCase, self).setUp()
        self.conn = mock.Mock()
        with open(
            "rsd_lib/tests/unit/json_samples/v2_4/volume_collection.json", "r"
        ) as f:
            self.conn.get.return_value.json.return_value = json.loads(f.read())

        self.volume_col = volume.VolumeCollection(
            self.conn,
            "/redfish/v1/StorageServices/NVMeoE1/Volumes",
            redfish_version="1.0.2",
        )

    def test__parse_attributes(self):
        self.assertEqual("1.0.2", self.volume_col.redfish_version)
        self.assertEqual("Volume Collection", self.volume_col.name)
        self.assertEqual(
            ("/redfish/v1/StorageServices/NVMeoE1/Volumes/1",),
            self.volume_col.members_identities,
        )

    @mock.patch.object(volume, "Volume", autospec=True)
    def test_get_member(self, mock_volume):
        self.volume_col.get_member(
            "/redfish/v1/StorageServices/NVMeoE1/Volumes/1"
        )
        mock_volume.assert_called_once_with(
            self.volume_col._conn,
            "/redfish/v1/StorageServices/NVMeoE1/Volumes/1",
            redfish_version=self.volume_col.redfish_version,
            registries=None,
        )

    @mock.patch.object(volume, "Volume", autospec=True)
    def test_get_members(self, mock_volume):
        members = self.volume_col.get_members()
        mock_volume.assert_called_once_with(
            self.volume_col._conn,
            "/redfish/v1/StorageServices/NVMeoE1/Volumes/1",
            redfish_version=self.volume_col.redfish_version,
            registries=None,
        )
        self.assertIsInstance(members, list)
        self.assertEqual(1, len(members))
