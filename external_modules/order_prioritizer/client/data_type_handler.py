# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

class DataTypeHandler:

    def __init__(self):
        self.custom_data_types = {"Name": [], "Class": []}

    async def client_load_custom_data_types_from_python_server(self, custom_type_definitions, client_custom_data_types):
        for name, obj in custom_type_definitions.items():
            client_custom_data_types["Name"].append(name)
            client_custom_data_types["Class"].append(obj)
        return client_custom_data_types

    async def client_load_custom_data_types_from_open62541_server(self, service_server_cust_data_types, client_custom_data_types):
        for i in service_server_cust_data_types:
            if isinstance(i, dict):
                for (name) in i.keys():
                    if name != 'ua' and name != 'datetime' and name != 'uuid' and name != 'IntEnum' \
                            and name != 'dataclass' and name != 'field' and name != 'List' and name != 'Optional' and name != '__builtins__':
                        client_custom_data_types["Name"].append(name)
                        client_custom_data_types["Class"].append(i[name])
        return client_custom_data_types

    async def load_custom_data_types(self, implementation, client):
        if implementation == "python":
            cust_enums = await client.load_enums()
            self.custom_data_types = await self.client_load_custom_data_types_from_python_server(cust_enums,
                                                                                                 self.custom_data_types)
            service_server_cust_data_types = await client.load_data_type_definitions()
            self.custom_data_types = await self.client_load_custom_data_types_from_python_server(
                service_server_cust_data_types, self.custom_data_types)
        elif implementation == "open62541":
            service_server_cust_data_types = await client.load_type_definitions()
            self.custom_data_types = await self.client_load_custom_data_types_from_open62541_server(
                service_server_cust_data_types, self.custom_data_types)
        return self.custom_data_types

    async def get_types(self, client):
        build_information = client.get_node("ns=0;i=2256")
        impl = await build_information.read_value()
        stack = impl.BuildInfo.ManufacturerName
        implementation = str(stack) if str(stack) == 'open62541' else "python"
        self.custom_data_types = await self.load_custom_data_types(implementation, client)

    def get_data_type_object(self, target_name):
        for i in range(len(self.custom_data_types["Name"])):
            if(str(self.custom_data_types["Name"][i]) == target_name):
                return self.custom_data_types["Class"][i]()

    def create_queue_objects(self, queue):
        if isinstance(queue, list):
            for i in range(len(queue)):
                obj = self.get_data_type_object("Queue_Data_Type")
                obj.Client_Identifier = queue[i].Client_Identifier
                obj.Service_UUID = queue[i].Service_UUID
                obj.Entry_Number = queue[i].Entry_Number
                obj.Queue_Element_State = queue[i].Queue_Element_State
                obj.ProductId = queue[i].ProductId
                obj.ServiceParameter = queue[i].ServiceParameter
                queue[i] = obj
            return queue
        else:
            obj = self.get_data_type_object("Queue_Data_Type")
            obj.Client_Identifier = queue.Client_Identifier
            obj.Service_UUID = queue.Service_UUID
            obj.Entry_Number = queue.Entry_Number
            obj.Queue_Element_State = queue.Queue_Element_State
            obj.ProductId = queue.ProductId
            obj.ServiceParameter = queue.ServiceParameter
            return obj


