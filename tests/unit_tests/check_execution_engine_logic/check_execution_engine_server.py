# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import unittest, asyncio, uuid
from execution_engine_logic.execution_engine_server import ExecutionEngineServer
from execution_engine_logic.data_object.data_object_interaction import DataObject
from execution_engine_logic.data_types.internal_data_converter import EngineOpcUaDataConverter
from tests.test_helpers.util.server_explorer import CheckServerNamespace
from asyncua import ua

class CheckExecutionEngineServer(unittest.TestCase):

    async def start_server_without_types(self, cov):
        cov.start()
        iteration_time = 0.001
        server_url = "opc.tcp://localhost:4000"
        server_instance = ExecutionEngineServer(execution_engine_server_url = server_url, log_info=True, iteration_time=iteration_time)
        await server_instance.init_server()
        #empty struct list
        server = await server_instance.start_server([], DataObject(EngineOpcUaDataConverter()))
        object_browse_names = [ua.QualifiedName(NamespaceIndex=2, Name='LifeCycleObject')]
        object_types_browse_names = [ua.QualifiedName(NamespaceIndex=2, Name='DataObject'), ua.QualifiedName(NamespaceIndex=2, Name='TaskObjectType')]
        async with server:
            #add a dummy production task
            production_task_uuid = str(uuid.uuid4())
            task_uuid = str(uuid.uuid4())
            object_browse_names.append(ua.QualifiedName(NamespaceIndex=2, Name=production_task_uuid))
            object_browse_names.append(ua.QualifiedName(NamespaceIndex=2, Name=task_uuid))
            await server_instance.data_object.opcua_declarations.instantiate_task_object(production_task_uuid, "productionTask", production_task_uuid)
            #add a additional task to the production task
            await server_instance.data_object.opcua_declarations.instantiate_task_object(task_uuid, "testTask", production_task_uuid)
            namespace = CheckServerNamespace(server_instance.idx)
            await namespace.start_client(server_url, server.nodes.root)
            for i in range(len(object_browse_names)):
                self.assertEqual(self.return_target_node(namespace.objects, object_browse_names[i]), object_browse_names[i])
            for i in range(len(object_types_browse_names)):
                self.assertEqual(self.return_target_node(namespace.objectTypes, object_types_browse_names[i]), object_types_browse_names[i])
        await server_instance.stop_server()
        cov.stop()

    def return_target_node(self, node_list, target_node):
        for i in range(len(node_list)):
            if target_node == node_list[i]:
                return node_list[i]
        return None

    def check_start_simple_server(self, cov):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start_server_without_types(cov))


