# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

from asyncua import Server
from execution_engine_logic.service_execution.execution_results import ExecutionParameterList
from execution_engine_logic.data_types.generate_opcua_server_types import GeneratePfdlTypes


class ExecutionEngineServer:

    def __init__(self, execution_engine_server_url, iteration_time, log_info):
        self.server_url = execution_engine_server_url
        self.log_info = log_info
        self.iteration_time = iteration_time
        self.server = None
        self.idx = None
        self.data_object = None
        self.custom_data_types = None
        self.sync_result_data_type_exists = None
        self.async_result_data_type_exists = None
        self.parameters = ExecutionParameterList()
        self.service_execution_states = [
            "ReadyForExecution",
            "ExecutionInProgess",
            "ExecutionCompleted"
        ]

    async def init_server(self):
        self.server = Server()
        await self.server.init()
        self.server.set_server_name("Execution Engine")
        self.server.set_endpoint(self.server_url)
        self.idx = await self.server.register_namespace("http://exection_engine.fraunhofer.de")
        self.data_object = None

    async def start_server(self, struct_object, data_object):
        await self.init_server()
        self.data_object = data_object
        self.data_object.set_idx(self.idx)
        self.data_object.set_server(self.server)
        await GeneratePfdlTypes(self.server, self.idx).create_parameter_struct_data_types(struct_object)
        self.custom_data_types = await self.data_object.opcua_declarations.load_custom_data_types()
        await self.data_object.opcua_declarations.instantiate_data_object()
        return self.server

    async def stop_server(self):
        self.custom_data_types = None
        await self.server.stop()



