# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import unittest, asyncio
from values.ee_structures import DemoScenarioStructureValues, DemoScenarioStructureTypes
from data_types.types import EngineArray, EngineStruct
from data_types.internal_data_converter import EngineOpcUaDataConverter, OpcUaEngineDataConverter
from execution_engine_server import ExecutionEngineServer
from data_object.data_object_interaction import DataObject
class CheckInternalDataConverter(unittest.TestCase):

    async def check_internal_data_transformer(self, custom_type_definitions= None):
        iteration_time = 0.001
        server_url = "opc.tcp://localhost:4002"
        server_instance = ExecutionEngineServer(execution_engine_server_url=server_url, log_info=True,
                                                iteration_time=iteration_time)
        await server_instance.init_server()
        types = DemoScenarioStructureTypes()
        server = await server_instance.start_server(types.structures, DataObject(EngineOpcUaDataConverter()))
        if custom_type_definitions == None:
            custom_type_definitions = server_instance.custom_data_types
        else:
            server_instance.custom_data_types = custom_type_definitions
        opcua_converter = EngineOpcUaDataConverter()
        ee_converter = OpcUaEngineDataConverter()
        structure_values = DemoScenarioStructureValues()
        generated_opcua_values, generated_ee_struct_values = [], []
        async with server:
            # convert all structures to opcua values
            for name, obj in structure_values.__dict__.items():
                value = opcua_converter.convert_to_opcua_struct(obj, custom_type_definitions, obj.data_type)
                generated_opcua_values.append(value)
                self.check_generated_opcua(value, obj)
            # convert the generated opc ua values back to engine values
            ctr = 0
            for name, obj in structure_values.__dict__.items():
                value = ee_converter.convert_opcua_to_ee(str(type(generated_opcua_values[ctr]).__name__), generated_opcua_values[ctr], server_instance)
                generated_ee_struct_values.append(value)
                self.check_generated_engine_types(obj, value)
                ctr += 1
            await server_instance.stop_server()
        return custom_type_definitions

    def check_generated_engine_types(self, obj, ee_struct):
        #self.assertEqual(obj.data_type, ee_struct.data_type)
        if isinstance(obj, EngineStruct):
            for name, obj in obj.attributes.items():
                if isinstance(obj, EngineStruct):
                    self.check_generated_engine_types(obj, ee_struct.attributes[name])
                elif isinstance(obj, EngineArray):
                    self.assertEqual(obj.name, ee_struct.attributes[name].name)
                    for i in range(len(obj.values)):
                        self.check_generated_engine_types(obj.values[i], ee_struct.attributes[name].values[i])
                else:
                    self.assertEqual(obj, ee_struct.attributes[name])
        else: self.assertEqual(obj, ee_struct)

    def check_generated_opcua(self, obj, ee_struct):
        for name, obj in obj.__dict__.items():
            if isinstance(ee_struct.attributes[name], EngineStruct):
                self.check_generated_opcua(obj, ee_struct.attributes[name])
            elif isinstance(ee_struct.attributes[name], EngineArray):
                for i in range(ee_struct.attributes[name].length):
                    self.check_generated_opcua(obj[i], ee_struct.attributes[name].values[i])
            else:
                self.assertEqual(obj, ee_struct.attributes[name])

    def check_start_simple_server(self, custom_type_definitions = None):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.check_internal_data_transformer(custom_type_definitions))
