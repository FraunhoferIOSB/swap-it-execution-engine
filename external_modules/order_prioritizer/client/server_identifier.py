# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from asyncua import Client
from external_modules.order_prioritizer.client.queue_prioritizer import QueuePrioritizer

class ServerFinder:

    def __init__(self, server_class):
        self.server_class = server_class
        self.client = None
        self.agent_node = None

    async def browse_registry(self, device_registry_url):
        if self.client == None:
            self.client = Client(device_registry_url)
        async with self.client:
            self.agent_node = await self.client.nodes.root.get_child("/Objects/AgentList/PFDLServiceAgents") if self.agent_node == None else self.agent_node
            children = await self.agent_node.get_children()
            for child in children:
                bn = await child.read_browse_name()
                if str(bn.Name) != "Filter_Agents" and str(bn.Name) != "Add_Agent_Server" and str(
                        bn.Name) != "Remove_Agent_Server":
                    servers = await child.get_children()
                    for server_url in servers:
                        server_bn = await server_url.read_browse_name()
                        if self.server_class.custom_url != None:
                            url = str(server_bn.Name).split(":")
                            self.server_class.server_list.append(self.server_class.custom_url + url[len(url) - 1])
            await self.client.disconnect()

    def update_client_list(self):
        #case list are identical
        if self.server_class.client_list["TargetServer"] == self.server_class.server_list:
            self.server_class.server_list = []
        #case server was added or removed since last iteration
        elif len(self.server_class.client_list["TargetServer"]) != len(self.server_class.server_list):
            new_client_list = {"Client":[], "TargetServer":[]}
            idx_list = []
            #add clients that already exist to the new_client_list
            for i in range(len(self.server_class.client_list["TargetServer"])):
                for j in range(len(self.server_class.server_list)):
                    if str(self.server_class.client_list["TargetServer"][i]) == str(self.server_class.server_list[j]):
                        new_client_list["Client"].append(self.server_class.client_list["Client"][i])
                        new_client_list["TargetServer"].append(self.server_class.client_list["TargetServer"][i])
                        idx_list.append(i)
            for i in range(len(idx_list) - 1 , -1, -1):
                del self.server_class.server_list[i]
            #add newly started client to the list
            idx_list = []
            for i in range(len(self.server_class.server_list)):
                client = QueuePrioritizer(self.server_class.server_list[i], self.server_class)
                client.start_client_thread()
                new_client_list["Client"].append(client)
                new_client_list["TargetServer"].append(self.server_class.server_list[i])
                idx_list.append(i)
            for i in range(len(idx_list) - 1 , -1, -1):
                del self.server_class.server_list[i]
            self.server_class.client_list = new_client_list


