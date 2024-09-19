# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import unittest
from execution_engine_logic.execution_engine_server import ExecutionEngineServer
from execution_engine_logic.data_object.data_object_interaction import DataObject
from tests.test_helpers.values.ee_structures import DemoScenarioStructureTypes
from execution_engine_logic.data_types.internal_data_converter import EngineOpcUaDataConverter

class Helper(unittest.TestCase):

    async def run_execution_engine_server(self, custom_data_types, iteration_time, server_url):
        server_instance = ExecutionEngineServer(execution_engine_server_url=server_url, log_info=True,
                                                iteration_time=iteration_time)
        await server_instance.init_server()
        types = DemoScenarioStructureTypes()
        server = await server_instance.start_server(types.structures, DataObject(EngineOpcUaDataConverter()))
        if custom_data_types == None:
            custom_data_types = server_instance.custom_data_types
        return custom_data_types, server_instance, server


    def examine_browsing_results(self, src_values, result_values):
        for i in range(len(src_values)):
            found = False
            for j in range(len(result_values)):
                if str(src_values[i]) == str(result_values[j].Name):
                    found = True
                    break
            self.assertEqual(found, True)