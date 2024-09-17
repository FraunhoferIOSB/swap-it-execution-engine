# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

from execution_engine_logic.data_types.types import EngineArray, EngineStruct

class EngineOpcUaDataConverter:

    def create_opcua_format(self, server, value):
        return self.convert_to_opcua_struct(value, server.custom_data_types, value.data_type)
    def instantiate_struct(self, struct, kwargs):
        val = struct(**kwargs)
        return val
    def create_kwargs(self,names, values):
        kwargs = {}
        for i in range(len(names)):
            kwargs[names[i]] = values[i]
        return kwargs
    def convert_to_opcua_struct(self, struct, custom_types, target_type):
        names, values = [], []
        for name, value in struct.attributes.items():
            names.append(name)
            if isinstance(value, EngineStruct):
                values.append(self.resolve_struct(value, custom_types, value.data_type))
            elif isinstance(value, EngineArray):
                values.append(self.resolve_array(value.values, custom_types, value.data_type))
            else:
                values.append(value)
        return self.instantiate_struct(self.get_custom_type_object(str(target_type), custom_types), self.create_kwargs(names, values))

    def resolve_array(self, array, custom_types, target_type):
        array_value = []
        if(isinstance(array[0], EngineStruct)):
            for i in range(len(array)):
                array_value.append(self.resolve_struct(array[i], custom_types, target_type))
        else:
            for i in range(len(array)):
                array_value = array.values
        return array_value

    def resolve_struct(self, struct, custom_types, target_type):
        names, values = [], []
        for name, value in struct.attributes.items():
            names.append(name)
            if isinstance(value, EngineStruct):
                values.append(self.resolve_struct(value, custom_types, value.data_type))
            elif isinstance(value, EngineArray):
                values.append(self.resolve_array(value.values, custom_types, value.data_type))
            else:
                values.append(value)
        return self.instantiate_struct(self.get_custom_type_object(str(target_type), custom_types), self.create_kwargs(names, values))

    def get_custom_type_object(self, name, custom_types):
        for i in range(len(custom_types["Name"])):
            if(str(name) == str(custom_types["Name"][i])):
                return custom_types["Class"][i]

class OpcUaEngineDataConverter:

    def convert_opcua_to_ee(self, variable_name, struct, server):
        variable = EngineStruct(variable_name)
        variable.data_type = server.data_object.get_name_fromNodeId(struct.data_type) if hasattr(struct, "data_type") else type(struct).__name__
        structure_type = False
        for i in server.custom_data_types["Class"]:
            if isinstance(struct, i):
                structure_type = True
        if structure_type:
            for (name, value) in struct.__dict__.items():
                if isinstance(value, str) or isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
                    variable.attributes[name] = value
                elif isinstance(value, list):
                    vals = EngineArray(name, len(value))
                    vals.data_type = server.data_object.get_name_fromNodeId(value[0].data_type) if hasattr(struct, "data_type") else type(value[0]).__name__
                    for i in range(len(value)):
                        vals.values.append(self.convert_opcua_to_ee(name, value[i], server))
                        variable.attributes[name] = vals
                else:
                    variable.attributes[name] = self.convert_opcua_to_ee(name, value, server)
        else:
            variable = struct
        return variable




