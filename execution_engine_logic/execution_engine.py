# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import asyncio
from datetime import datetime
from asyncua import ua
from execution_engine_logic.data_types.generate_opcua_server_types import ExtractPFDL
from execution_engine_logic.data_types.internal_data_converter import EngineOpcUaDataConverter
from execution_engine_logic.execution_engine_server import ExecutionEngineServer
from execution_engine_logic.data_object.data_object_interaction import DataObject
from control_interface.control_interface import ControlInterface
from control_interface.target_server.target_server_dict import TargetServerList

class ExecutionEngine:

    def __init__(self, server_url, iteration_time, log_info, number_default_clients, device_registry_url, assignment_agent_url,
                dispatcher_object, delay_start):
        self.log_info = log_info
        self.server_url = server_url
        self.iteration_time = iteration_time
        self.server = None
        self.server_instance = None
        self.number_default_clients = number_default_clients
        self.running = True
        self.device_registry_url = device_registry_url
        self.assignment_agent_url = assignment_agent_url
        self.delay_start = delay_start
        self.dispatcher = dispatcher_object

    async def start_server(self, struct_object, data_object):
        self.server = ExecutionEngineServer(self.server_url, self.iteration_time, self.log_info)
        self.server_instance = await self.server.start_server(struct_object, data_object)
        print("[", datetime.now(), "] Start Execution Engine ", self.server_instance)

    async def main(self):
        if self.delay_start != None:
            await asyncio.sleep(self.delay_start)
        process_pfdl = ExtractPFDL()
        struct_dict = process_pfdl.create_struct_dict(self.dispatcher.structs)
        await self.start_server(struct_dict, DataObject(EngineOpcUaDataConverter()))
        self.dispatcher.set_callbacks(self.server_instance, self.server, process_pfdl, self)
        ClientControlInterface = ControlInterface(self.server, self.server_instance, self.dispatcher.dispatcher_callbacks.service_execution_list, TargetServerList(self.server), self.running, self.device_registry_url, self.assignment_agent_url)
        if self.number_default_clients > 0:
            ClientControlInterface.init_default_clients(self.number_default_clients)
        self.dispatcher.dispatcher_callbacks.add_control_interface(ClientControlInterface)
        self.dispatcher.run_dispatcher()
        async with self.server_instance:
            while self.dispatcher.running():
                service_uuid, task_uuid, name = self.dispatcher.dispatcher_callbacks.service_execution_list.remove_service()
                if service_uuid != None:
                    await self.server.data_object.write_state_variable(task_uuid, ua.Variant(self.server.service_execution_states[0]))
                    if self.log_info:
                        print("[", datetime.now(), "] ---------> Set Token for Service ", name, " with uuid ", service_uuid)
                    self.dispatcher.fire_event(service_uuid)
                await asyncio.sleep(self.iteration_time)
            print("[", datetime.now(), "] Shut down the ControlInterface ")
            for i in range(len(ClientControlInterface.client_dict["Client"])):
                ClientControlInterface.client_dict["Client"][i].stop_control_interface_loop()
            print("[", datetime.now(), "] Shut down the Execution Engine ", self.server_instance)
            await self.server.stop_server()
            print("[", datetime.now(), "] Order Agent Stopped")

