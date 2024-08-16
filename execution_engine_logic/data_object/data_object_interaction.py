# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import uuid
from asyncua import ua
from execution_engine_logic.data_object.instantiate_objects import InstantiateTypes

class DataObject:

    def __init__(self, converter):
        self.server = None
        self.idx = None
        self.opcua_declarations = None
        self.opc_ua_converter = converter
        self.state_variable_bn = "StateVariable"
        self.type_list = {"Name":[], "NodeId":[]}

    def set_idx(self, idx):
        self.idx = idx

    def set_server(self, server):
        self.server = server
        self.opcua_declarations = InstantiateTypes(self.server, self.idx)

    async def write_state_variable(self, task, new_state):
        state_var_node_id = await self.get_child_nodeid_from_browsename(task, self.state_variable_bn)
        await state_var_node_id.write_value(new_state, ua.VariantType.String)

    async def get_child_nodeid_from_browsename(self, task_uuid, child_browsename):
        task_node = self.server.get_node(ua.NodeId(Identifier=uuid.UUID(task_uuid), NamespaceIndex=self.idx, NodeIdType=ua.NodeIdType.Guid))
        children = await task_node.get_children()
        for child in children:
            available_browse_names = await child.read_browse_name()
            if str(available_browse_names.Name) == str(child_browsename):
                return child

    async def remove_node(self, node):
        node = self.server.get_node(node)
        await self.server.delete_nodes([node])

    async def read_struct_values(self, task_uuid,variable_name):
        struct = self.server.get_node(
            ua.NodeId(Identifier=uuid.UUID(task_uuid), NamespaceIndex=self.idx, NodeIdType=ua.NodeIdType.Guid))
        children = await struct.get_children()
        for child in children:
            bn = await child.read_browse_name()
            if str(bn.Name) == str(variable_name):
                variable_value = await child.read_value()
                return variable_value

    async def add_struct_variable(self, names, data_types, values, context, server_instance, server):
        current_task_node = server_instance.get_node(
            ua.NodeId(Identifier=uuid.UUID(context), NamespaceIndex= self.idx, NodeIdType=ua.NodeIdType.Guid))
        for i in range(len(names)):
            if isinstance(data_types[i], ua.NodeId):
                node_id = data_types[i]
            else:
                node_id = self.get_nodeId_fromType(data_types[i])
                if node_id is None:
                    node_id = await server_instance.nodes.root.get_child([*server.data_object.opcua_declarations.path_to_custom_structs, str(self.idx) + ":" + str(data_types[i])])
                node_id = ua.NodeId.from_string(str(node_id))
            await current_task_node.add_variable(self.idx, names[i], values[i], datatype=node_id)

    def get_nodeId_fromType(self, name):
        for i in range(len(self.opcua_declarations.custom_data_types["Name"])):
            if str(self.opcua_declarations.custom_data_types["Name"][i]) == str(name):
                return self.opcua_declarations.custom_data_types["NodeId"][i]

    def get_name_fromNodeId(self, nodeId):
        for i in range(len(self.opcua_declarations.custom_data_types["NodeId"])):
            if self.opcua_declarations.custom_data_types["NodeId"][i].nodeid == nodeId:
                return self.opcua_declarations.custom_data_types["Name"][i]


