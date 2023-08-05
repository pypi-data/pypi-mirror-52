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

import logging

from sushy.resources import base
from sushy import utils

from rsd_lib import base as rsd_lib_base

LOG = logging.getLogger(__name__)

NAME_MAPPING = {
    "Name": "name",
    "Required": "required",
    "DataType": "data_type",
    "ObjectDataType": "object_data_type",
    "AllowableValues": "allowable_values",
}


class AttachResourceActionInfo(rsd_lib_base.ResourceBase):

    identity = base.Field("Id", required=True)
    """The storage pool  identity string"""

    description = base.Field("Description")
    """The storage pool  description string"""

    name = base.Field("Name")
    """The storage pool  name string"""

    @property
    @utils.cache_it
    def parameters(self):
        """Property to provide reference to `Parameters` instance

        It is calculated once when it is queried for the first time. On
        refresh, this property is reset.
        """
        parameters = []
        for i in self.json.get("Parameters"):
            item = {}
            for key in NAME_MAPPING:
                item[NAME_MAPPING[key]] = i[key]

            if item["name"] == "Resource":
                item["allowable_values"] = utils.get_members_identities(
                    item["allowable_values"]
                )

            parameters.append(item)

        return parameters
