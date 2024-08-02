# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from dispatcher.dispatcher_callbacks.cb_util import CallbackHelpers
from execution_engine_logic.service_execution.execution_dict import ServiceInfo, ExecutionList
from datetime import datetime
import uuid
from asyncua import ua

class DispatcherCallbackFunctions:
    def __init__(self, server_instance: object, server: object, read_pfdl: object, execution_engine: object, data_object, opcua_data_converter, ee_data_converter) -> object:
        self.server = server
        self.server_instance = server_instance
        self.read_pfdl = read_pfdl
        self.idx = self.server.idx
        self.service_execution_list = ExecutionList()
        self.execution_engine = execution_engine
        self.data_object = data_object
        self.callback_helpers = CallbackHelpers(self.server, self.read_pfdl, self.data_object)
        self.target_server_list = None
        self.control_interface = None
        self.opcua_data_converter = opcua_data_converter
        self.ee_data_converter = ee_data_converter

    def add_control_interface(self, ControlInterface):
        self.control_interface = ControlInterface
        self.target_server_list = self.control_interface.target_server_list

    async def task_finished_cb(self, name:str, task_identifier, context:str, output_parameters):
        if self.server.log_info:
            print("[", datetime.now(), "] Task " + context +" with UUID: " + task_identifier + " finished in context ", context)
        if len(output_parameters) != 0 and name != "productionTask":
            for variable in output_parameters:
                val = await self.server.data_object.read_struct_values(task_identifier, str(variable))
                existing_val = await self.server.data_object.read_struct_values(context, str(variable))
                if existing_val != None:
                    await self.server.data_object.remove_node(existing_val.data_type)
                await self.server.data_object.add_struct_variable([variable], [val.data_type], [val],
                                                                context, self.server_instance, self.server)
        if name != "productionTask":
            await self.server.data_object.remove_node(ua.NodeId(Identifier=uuid.UUID(task_identifier), NamespaceIndex=self.idx, NodeIdType=ua.NodeIdType.Guid))

    async def task_started_cb(self, name:str, task_identifier, context:str, input_parameters, parameters_instances):
        if self.server.log_info:
            print("[", datetime.now(), "] Task " + name +" with UUID: " + task_identifier + " started in context ", context)
        await self.server.data_object.opcua_declarations.instantiate_task_object(task_identifier, name, context)
        if name != "productionTask":
            variables = await self.callback_helpers.create_task_variables(parameters_instances, context, self.server, self.server_instance, self.opcua_data_converter)
            await self.server.data_object.add_struct_variable(*self.callback_helpers.get_input_names_and_types(input_parameters), variables['Input_Value'], task_identifier, self.server_instance, self.server)

    async def service_started_cb(self, name, service_uuid, context, input_parameters, output_parameters):
        if self.server.log_info:
            print("[", datetime.now(), "] Service " + name + " with UUID " + service_uuid + " started in context " + context)
        self.service_execution_list.add_service(ServiceInfo(service_uuid, context, False, name))
        names, values = await self.callback_helpers.read_struct_value_from_data_object(*self.callback_helpers.classify_service_input(input_parameters), context)
        o_parameters = self.callback_helpers.read_service_output_parameter(output_parameters)
        self.tar_server_url = self.callback_helpers.check_for_resource_assignment(self.server, values)
        self.control_interface.start_client_interaction(name, str(self.tar_server_url), [names, values], context, service_uuid, o_parameters)

    async def service_finished_cb(self, name, context, service_identifier):
        if self.server.log_info:
            print("[", datetime.now(), "] Service " + name + " with UUID " + service_identifier + " finished  in context " + context)
        for parameter in self.server.parameters.parameters:
            if str(parameter.context) == str(context) and str(parameter.service_uuid) == str(service_identifier):
                for variable in range(len(parameter.variables)):
                    val = await self.server.data_object.read_struct_values(parameter.context, parameter.variables[variable])
                    if val != None:
                        await self.server.data_object.remove_node(self.server.data_object.get_nodeId_fromType(str(parameter.type[variable])))
                    await self.server.data_object.add_struct_variable([parameter.variables[variable]], [parameter.type[variable]], [parameter.results[variable]],
                                                                    parameter.context, self.server_instance, self.server)
                self.server.parameters.remove_parameter(parameter.service_uuid)

    async def read_struct_parameter_from_server(self, variable_name, task_api):
        return self.ee_data_converter.convert_opcua_to_ee(variable_name, await self.server.data_object.read_struct_values(task_api.uuid, variable_name), self.server)

    def provide_parameter(self, service_id, task_id):
        return self.read_struct_parameter_from_server(service_id, task_id)
