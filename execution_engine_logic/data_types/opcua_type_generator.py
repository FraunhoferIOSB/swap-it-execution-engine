# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

from asyncua import ua, Server
from asyncua.common.structures104 import new_struct, new_struct_field
from execution_engine_logic.data_types.types import EngineArray, EngineStruct

class TypeGenerator:

    def __init__(self, execution_engine):
        self.types = {}
        self.supported_simple_types = ["string", "number", "boolean"]
        self.opcua_types = {"string": "String", "number": "Double", "boolean": "Boolean"}
        self.execution_engine = execution_engine

    async def create_opcua_types(self, dispatcher_structs):
        self.interprete_custom_structure(dispatcher_structs)
        await self.generate_opcua_types()
    def interprete_custom_structure(self, dispatcher_structs):
        for i in range(len(dispatcher_structs)):
            type = DataTypeObject(dispatcher_structs[i].name, dispatcher_structs[i].data_type, "Struct")
            for key, value in dispatcher_structs[i].attributes.items():
                if isinstance(value, EngineArray):
                    type.attributes[key] = DataTypeObject(value.name, value.data_type, "Array")
                    type.attributes[key].set_array_length(value.length)
                elif self.check_simple_type(value) != None:
                    type.attributes[key] = DataTypeObject(key, value, "Simple")
                else:
                    type.attributes[key] = DataTypeObject(key, value, "Struct")
            self.types[dispatcher_structs[i].name] = type
        self.types = self.sort_custom_types()

    async def generate_opcua_types(self):
        generated_types = {}
        for key, value in self.types.items():
            struct_fields = []
            for attr, val in value.attributes.items():
                struct_fields.append(new_struct_field(attr,
                      ua.VariantType(ua.VariantType[self.opcua_types[val.type]].value) if val.construct == "Simple"
                      else generated_types[val.type], array = False if val.construct != "Array" else True))
            new_structure_node, _ = await new_struct(self.execution_engine.server, self.execution_engine.idx, key,
                                                     [*struct_fields])
            generated_types[key] = new_structure_node

    def check_simple_type(self, req_type):
        for i in range(len(self.supported_simple_types)):
            if str(self.supported_simple_types[i]) == str(req_type):
                return self.supported_simple_types[i]
        return None

    def sort_custom_types(self):
        sorted_elements = {}
        while len(sorted_elements.keys()) < len(self.types.keys()):
            for key, value in self.types.items():
                add = True
                for attr, val in value.attributes.items():
                    if str(val.construct) != "Simple":
                        add = self.check_existing_struct(val.type, sorted_elements)
                if add == True:
                    sorted_elements[key] = value
        return sorted_elements

    def check_existing_struct(self, req_str, struct_list):
        for key, value in struct_list.items():
            if str(key) == str(req_str):
                return True
        return False

class DataTypeObject:

    def __init__(self, name, type, construct):
        self.name = name
        self.type = type
        self.construct = construct
        self.array_length = None
        self.attributes = {}

    def set_array_length(self, array_length):
        self.array_length = array_length


