# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from asyncua import ua, Client
import asyncio, threading
from external_modules.order_prioritizer.client.target_server_explorer import TargetServerExplorer

class QueuePrioritizer:

    def __init__(self, target_server_url, server_class):
        self.server_class = server_class
        self.update = False
        self.running = True
        self.target_server_url = target_server_url
        self.priority_list = None
        self.custom_data_types = {"Name": [], "Class": []}

    def start_client_thread(self):
        client_thread = threading.Thread(target=self.start_new_client_loop, daemon=True)
        client_thread.start()

    def start_new_client_loop(self):
        control_interface_loop = asyncio.new_event_loop()
        control_interface_loop.run_until_complete(self.run_client())

    async def run_client(self):
        async with Client(self.target_server_url) as client:
            explorer = TargetServerExplorer()
            await explorer.data_type_handler.get_types(client)
            self.queue_variable = await explorer.get_queue(client)
            while self.running:
                if self.update:
                        #call the sort_queue_elements method within the server
                        if len(self.priority_list) != 0:
                            opc_ua_prio_list = []
                            for element in self.priority_list:
                                change = explorer.data_type_handler.get_data_type_object("Change_Queue_Data_Type")
                                change.OrderId = element[0]
                                change.PrioritizationValue = int(element[1])
                                opc_ua_prio_list.append(change)
                            var = ua.Variant(Value=opc_ua_prio_list, is_array=True)
                            service_object_node = client.get_node(explorer.service_queue)
                            await service_object_node.call_method("2:sort_queue_elements", var)
                        self.update = False
                await asyncio.sleep(1)



