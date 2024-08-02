# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from execution_engine_logic.data_types.types import EngineStruct

class CallbackHelpers:

    def __init__(self, server, read_pfdl, data_object):
        self.server = server
        self.read_pfdl = read_pfdl
        self.data_object = data_object

    def get_input_names_and_types(self, input_parameters):
        data_types, names = [], []
        for key, value in input_parameters.items():
            names.append(key)
            data_types.append(value)
        return names, data_types

    async def create_task_variables(self, input_parameters, context, server, server_instance, opcua_data_converter):
        task_input_type = {"Input": [], "Input_Value": []}
        for item in input_parameters:
            if isinstance(item, EngineStruct):
                task_input_type["Input"].append("Literal")
                task_input_type["Input_Value"].append(item)
            else:
                task_input_type["Input"].append(item)
                task_input_type["Input_Value"].append("Read from task context")
        for i in range(len(task_input_type['Input_Value'])):
            if (str(task_input_type['Input_Value'][i]) == "Read from task context"):
                task_input_type['Input_Value'][i] = await self.data_object.read_struct_values(context, str(
                    task_input_type['Input'][i]))
            else:
                task_input_type['Input_Value'][i] = opcua_data_converter.create_opcua_format(server, task_input_type['Input_Value'][i])
        return task_input_type

    def classify_service_input(self, input_parameter):
        Task_Input_Structs, Task_Input_Structs_Values = [], []
        for i in range(len(input_parameter)):
            if isinstance(input_parameter[i], str):
                Task_Input_Structs.append(input_parameter[i])
                Task_Input_Structs_Values.append("Read from Data Lifecycle Object")
            else:
                Task_Input_Structs.append("Literal")
                Task_Input_Structs_Values.append(input_parameter[i])
        return Task_Input_Structs, Task_Input_Structs_Values

    async def read_struct_value_from_data_object(self, names, values, context):
        for i in range(len(names)):
            if isinstance(values[i], list):
                value = await self.data_object.read_struct_values(context, values[i][0])
                path = values[i][1:]
                for j in range(len(path)):
                    for key, val in value.__dict__.items():
                        if str(key) == str(path[j]):
                            value = val
                            break
                values[i] = value
            #single structure
            elif isinstance(values[i], str):
                values[i] = await self.data_object.read_struct_values(context, names[i])
        return names, values

    def read_service_output_parameter(self, element_value):
        self.element_value = element_value
        variable_name, struct_name, task_output_parameters = [], [], []
        for (item, it_value) in self.element_value.items():
            variable_name.append(item)
            struct_name.append(it_value)
        task_output_parameters.append(variable_name)
        task_output_parameters.append(struct_name)
        return task_output_parameters

    def check_for_resource_assignment(self, server, input_parameter):
        res = None
        for i in range(len(server.custom_data_types["Name"])):
            if str(server.custom_data_types["Name"][i]) == "ResourceAssignment":
                res = server.custom_data_types["Class"][i]()
        for i in range(len(input_parameter)):
            if isinstance(input_parameter[i], type(res)):
                for key, value in input_parameter[i].__dict__.items():
                    return value


