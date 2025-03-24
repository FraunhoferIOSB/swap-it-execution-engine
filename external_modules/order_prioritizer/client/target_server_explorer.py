# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from asyncua import ua
from external_modules.order_prioritizer.client.data_type_handler import DataTypeHandler

class TargetServerExplorer:

    def __init__(self):
        self.common_namespace_idx = None
        self.has_subtype_id = "ns=0;i=45"
        self.has_typedef_id = "ns=0;i=40"
        self.path_to_queue_variable = ["Queue", "ServiceQueue", "queue_variable"]
        self.path_to_sort_method = ["Queue", "ServiceQueue", "sort_queue_elements"]
        self.path_to_service_queue = ["Queue", "ServiceQueue"]
        self.service_queue = None
        self.sort_method = None
        self.module_type_node_NodeId = None
        self.module = None
        self.data_type_handler = DataTypeHandler()

    async def get_queue(self, client):
        namespace_array = client.get_node("ns=0;i=2255")
        array = await namespace_array.read_value()
        for i in range(len(array)):
            if str(array[i]) == "http://common.swap.fraunhofer.de":
                self.common_namespace_idx = i
        module_type_node = await client.nodes.root.get_child("Types/ObjectTypes/BaseObjectType/"+str(self.common_namespace_idx)+":ModuleType")
        for reference in await module_type_node.get_references():
            if reference.IsForward == True:
                if str(reference.ReferenceTypeId.Identifier) == str(ua.NodeId.from_string(self.has_subtype_id).Identifier)\
                        and str(reference.ReferenceTypeId.NamespaceIndex) == str(ua.NodeId.from_string(self.has_subtype_id).NamespaceIndex):
                    refs = await client.get_node(reference.NodeId).get_references()
                    for ref in refs:
                        if ref.IsForward == False:
                            if str(ref.ReferenceTypeId.Identifier) == str(ua.NodeId.from_string(self.has_typedef_id).Identifier)\
                                    and str(ref.ReferenceTypeId.NamespaceIndex) == str(ua.NodeId.from_string(self.has_typedef_id).NamespaceIndex):
                                self.module = client.get_node(ref.NodeId)
        self.sort_method = await self.find_node_by_browsename_list(self.path_to_sort_method, client, self.module)
        self.service_queue = await self.find_node_by_browsename_list(self.path_to_service_queue, client, self.module)
        return await self.find_node_by_browsename_list(self.path_to_queue_variable, client, self.module)

    async def find_node_by_browsename_list(self, browse_list, client, current_node):
        if current_node == None:
            current_node = client.get_objects_node()
        for i in range(len(browse_list)):
            children = await current_node.get_children()
            for child in children:
                bn = await child.read_browse_name()
                if (str(bn.Name) == str(browse_list[i])):
                    current_node = child
        return current_node


