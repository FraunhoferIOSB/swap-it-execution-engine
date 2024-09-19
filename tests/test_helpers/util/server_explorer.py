# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

from asyncua import Client, ua

class CheckServerNamespace:

    def __init__(self, idx):
        self.server_namespace_idx = idx
        self.objects = []
        self.variables = []
        self.objectTypes = []
        self.dataTypes = []

    def reset(self, idx):
        self.server_namespace_idx = idx
        self.objects = []
        self.variables = []
        self.objectTypes = []
        self.dataTypes = []
    async def start_client(self, server_url, start_node, check_children = True):
        async with Client(url=server_url):
            await self.browse_namespace(start_node, check_children)

    async def browse_namespace(self, start_node, check_children = True):
        for child in await start_node.get_children():
            bn = await child.read_browse_name()
            if bn.NamespaceIndex == self.server_namespace_idx:
                node_class = await child.read_node_class()
                if  node_class == ua.NodeClass(1):
                    self.objects.append(bn)
                elif node_class == ua.NodeClass(2):
                    self.variables.append(bn)
                elif node_class == ua.NodeClass(64):
                    self.dataTypes.append(bn)
                elif node_class == ua.NodeClass(8):
                    self.objectTypes.append(bn)
            if check_children == True:
                await self.browse_namespace(child)

    async def find_node_by_browsename(self, start_node, target_node):
        for child in await start_node.get_children():
            child_bn = await child.read_browse_name()
            if str(target_node.Name) == str(child_bn.Name):
                return child
            await self.find_node_by_browsename(child, target_node)
        return None
