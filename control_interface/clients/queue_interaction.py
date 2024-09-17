# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
import asyncio, uuid
from asyncua import ua

class TargetServerQueue:
    def __init__(self, iteration_time, client):
        self.data_type = "Queue_Data_Type"
        self.iteration_time = iteration_time
        self.client = client

    async def client_add_queue_element(self, target_server, service_uuid):
        client_identifier = str(uuid.uuid4())
        for i in range(len(target_server.client_custom_data_types["Name"])):
            if(str(target_server.client_custom_data_types["Name"][i]) == self.data_type):
                entry = target_server.client_custom_data_types["Class"][i]()
                entry.Service_UUID=service_uuid
                entry.Client_Identifier=client_identifier
                entry.Queue_Element_State=await self.get_queue_state_enum(target_server)
                id = str(target_server.add_queue_element_bn.NamespaceIndex)+":"+str(target_server.add_queue_element_bn.Name)
                entry = ua.Variant(entry, ua.VariantType.ExtensionObject)
                await self.client.get_node(target_server.service_queue).call_method(id, entry)
        return client_identifier

    async def get_queue_state_enum(self, target_server):
        for i in range(len(target_server.client_custom_data_types["Name"])):
            if (str(target_server.client_custom_data_types["Name"][i]) == "Queue_State_Variable_Type"):
                state_variable_type = target_server.client_custom_data_types["Class"][i](0)
                return state_variable_type

    async def client_remove_queue_element(self, target_server, service_uuid, client_identifier):
        for i in range(len(target_server.client_custom_data_types["Name"])):
            if (str(target_server.client_custom_data_types["Name"][i]) == self.data_type):
                entry = target_server.client_custom_data_types["Class"][i](Service_UUID = service_uuid, Client_Identifier = client_identifier, Queue_Element_State = await self.get_queue_state_enum(target_server))
                id = str(target_server.remove_queue_element_bn.NamespaceIndex) + ":" + str(
                    target_server.remove_queue_element_bn.Name)
                entry = ua.Variant(entry, ua.VariantType.ExtensionObject)
                await self.client.get_node(target_server.service_queue).call_method(id, entry)

    async def wait_for_queue_position_one(self, target_server, client_uuid, service_uuid):
        first_element = False
        while first_element == False:
            queue = await self.client.get_node(target_server.queue_variable).read_value()
            if not isinstance(queue, list):
                if queue.Client_Identifier == client_uuid and queue.Service_UUID == service_uuid and queue.Entry_Number == 1:
                   first_element = True
            else:
                for i in range(len(queue)):
                    if queue[i].Client_Identifier == client_uuid and queue[i].Service_UUID == service_uuid and queue[i].Entry_Number == 1:
                        first_element = True
            await asyncio.sleep(self.iteration_time)

