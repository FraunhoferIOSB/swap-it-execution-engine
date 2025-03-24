# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import asyncio, time
from asyncua import ua, uamethod, Server, Client
from external_modules.order_prioritizer.server.create_address_space import Namespace
from external_modules.order_prioritizer.client.server_identifier import ServerFinder

class PrioritizerServer:

    def __init__(self, url, port, device_registry_url, custom_url = None, waiting_time = 5):
        self.url = url
        self.port = port
        self.device_registry_url = device_registry_url
        self.server = None
        self.custom_url = custom_url
        self.client_list = {"Client":[], "TargetServer":[]}
        self.server_finder = None
        self.server_list = []
        self.priority_list = None
        self.waiting_time = waiting_time

    def order_priority_list(self, priority_list):
        new_list = []
        ctr = 0
        max_val = max(priority_list, key=lambda x: int(x[1]))
        while ctr <= int(max_val[1]):
            for i in range(len(priority_list)):
                if priority_list[i][1] == str(ctr):
                    new_list.append(priority_list[i])
            ctr += 1
        return new_list

    async def run_server(self):
        self.server = Server()
        await self.server.init()
        self.server.set_endpoint(str(self.url)+str(self.port))

        async with self.server:
            namespc = Namespace(self.server)
            await namespc.add_namespace()
            ctr = 0
            while True:
                ctr += 1
                # update server queues
                if ctr % self.waiting_time == 0:
                    self.priority_list = await namespc.variable_node.read_value()
                    if self.priority_list != None and len(self.priority_list) > 0:
                        self.priority_list = self.order_priority_list(self.priority_list)
                        await namespc.variable_node.write_value(
                            ua.Variant(Value=self.priority_list, VariantType=ua.VariantType.String,
                                       Dimensions=[len(self.priority_list), 2], is_array=True))
                    for client in self.client_list["Client"]:
                        client.update = True
                        client.priority_list = self.priority_list
                # update client_list
                if ctr % self.waiting_time == 0:
                    if self.server_finder is None:
                        self.server_finder = ServerFinder(self)
                    await self.server_finder.browse_registry(self.device_registry_url)
                    self.server_finder.update_client_list()
                await asyncio.sleep(1)







