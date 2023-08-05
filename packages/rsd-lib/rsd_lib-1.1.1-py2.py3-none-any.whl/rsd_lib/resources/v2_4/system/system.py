# Copyright 2019 Intel, Inc.
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

from sushy import utils

from rsd_lib.resources.v2_3.system import system
from rsd_lib.resources.v2_4.system import processor


class System(system.System):

    @property
    @utils.cache_it
    def processors(self):
        """Property to provide reference to `ProcessorCollection` instance

           It is calculated once when it is queried for the first time. On
           refresh, this property is reset.
        """
        return processor.ProcessorCollection(
            self._conn,
            utils.get_sub_resource_path_by(self, "Processors"),
            redfish_version=self.redfish_version,
        )


class SystemCollection(system.SystemCollection):

    @property
    def _resource_type(self):
        return System
