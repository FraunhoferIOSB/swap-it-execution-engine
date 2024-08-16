# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from asyncua.sync import ua
class CheckServiceMethodArguments:

    def __init__(self, server):
        self.server = server

    async def browse_method_arguments(self, methodId, client, sync_node, async_node, event_node, service_bn, cust_types):
        methodId = client.get_node(methodId)
        args = await methodId.get_properties()
        arg_type = ['InputArguments', 'OutputArguments']
        inp = []
        outp = {"OutputArgumentType":[], "SyncArguments":[], "AsyncArguments":[]}
        for arg in args:
            browsename = await client.get_node(arg).read_browse_name()
            for option in arg_type:
                if browsename == ua.QualifiedName(option):
                    values = await arg.read_value()
                    for value in values:
                        dt_node = client.get_node(value.DataType)
                        browse = await dt_node.read_browse_name()
                        if option == arg_type[0]:
                            inp.append([value.Name, browse.Name])
                        else:
                            outp["OutputArgumentType"].append([value.Name, browse.Name])
                            found = False
                            current_node = dt_node
                            while found == False:
                                if current_node == client.get_node("i=22"):
                                    print("wrong output data type")
                                elif current_node == async_node:
                                    found = True
                                    outp["OutputArgumentType"] = "ServiceExecutionAsyncResultDataType"
                                    outp = await self.add_async_arg(await client.get_node(event_node).get_children(), service_bn, client, outp)
                                    outp = await self.add_sync_arg(client, cust_types, outp, dt_node)
                                elif current_node == sync_node:
                                    found = True
                                    outp = await self.add_sync_arg(client, cust_types, outp, dt_node)
                                current_node = await current_node.get_parent()
        return inp, outp

    async def add_sync_arg(self, client, cust_types, OutputArguments, data_type_node):
        struct_data_type_browse_name = await client.get_node(data_type_node).read_browse_name()
        data_type_variables = await self.extract_custom_struct_fields(struct_data_type_browse_name.Name, cust_types)
        for k in range(len(data_type_variables)):
            OutputArguments["SyncArguments"].append(data_type_variables[k])
        return OutputArguments

    async def add_async_arg(self, custom_events, service_browse_name, client, OutputArguments):
        for child in custom_events:
            child_bn = await child.read_browse_name()
            if str(child_bn.Name) == str(service_browse_name):
                self.event = child
                properties = await self.event.get_properties()
                for property in properties:
                    property_bn = await property.read_browse_name()
                    data_type_bn = await client.get_node(await property.read_data_type()).read_browse_name()
                    OutputArguments["AsyncArguments"].append([property_bn.Name, data_type_bn.Name])
        return OutputArguments

    async def extract_custom_struct_fields(self, struct_data_type, cust_types):
        field_array = []
        for (name, field) in self.get_custom_struct(struct_data_type, cust_types).__dataclass_fields__.items():
            field_array.append([name, field.type])
        return field_array

    async def check_input_arguments(self, dlo_service_input, InputArguments, custom_types):
        param = []
        for argument in InputArguments:
            # list in argument contains: [0] = name, [1] = DataType
            match = False
            datatype = self.get_custom_struct(argument[1], custom_types)
            if datatype is None:
                print("Invalid Type for Input Argument")
            for i in range(len(dlo_service_input[0])):
                if str(dlo_service_input[0][i]) == str('Literal'):
                    break
                elif str(argument[0]) == str(dlo_service_input[0][i]) and isinstance(dlo_service_input[1][i], type(datatype)):
                    match = True
                    param, dlo_service_input = self.add_input_argument(param, dlo_service_input, i)
                    break
            if match == False:
                for i in range(len(dlo_service_input[1])):
                    if isinstance(dlo_service_input[1][i], type(datatype)):
                        param, dlo_service_input = self.add_input_argument(param, dlo_service_input, i)
                        break
            elif match == False:
                    print("Missing Variable -> not able to execute service")
        return param

    def get_custom_struct(self, name, custom_types):
        for i in range(len(custom_types["Name"])):
            if (str(custom_types["Name"][i]) == str(name)):
                return custom_types["Class"][i]()

    def add_input_argument(self, param, dlo_service_input, pos):
        param.append(dlo_service_input[1][pos])
        self.del_list_elements(dlo_service_input, pos)
        return param, dlo_service_input

    async def extract_service_output(self, OutputArguments, service_results, dlo_service_output, custom_data_type):
        out = {"Variable_Name": [], "Variable_Value": [], "Variable_Data_Type": []}
        num_parameter = len(dlo_service_output[0])
        if (len(service_results["SyncReturn"]) > 0):
            for (attr, value) in service_results["SyncReturn"][0].__dict__.items():
                for i in range(len(dlo_service_output[0])):
                    if str(attr) == str(dlo_service_output[0][i]) and type(self.get_custom_struct(dlo_service_output[1][i], custom_data_type) == type(value)):
                        out = self.append_out(out, attr, value, type(value))
        for i in range(len(service_results["AsyncReturn"])):
            dlo_service_output, out = self.match_async_return(OutputArguments["AsyncArguments"], dlo_service_output, out, service_results["AsyncReturn"][i], custom_data_type)
        if(len(out["Variable_Name"]) != num_parameter):
            print("ERROR, unable to match all output parameters specified for the service")
        return out

    def match_async_return(self, OutputArguments, dlo_service_output, out, service_result, custom_data_type):
        for j in range(len(OutputArguments)):
            for z in range(len(dlo_service_output[0])):
                # match the output argument name and the with the name of the dlo_service_output
                if (str(OutputArguments[j][0]) == str(dlo_service_output[0][z])
                        and str(OutputArguments[j][1]) == str(dlo_service_output[1][z])):
                    if (type(self.get_custom_struct(OutputArguments[j][1], custom_data_type)) == type(service_result)
                            or str(type(self.get_custom_struct(OutputArguments[j][1], custom_data_type))) == str(type(service_result))):
                        out = self.append_out(out, OutputArguments[j][0], service_result, dlo_service_output[1][z])
                        self.del_list_elements(dlo_service_output, z)
                        return dlo_service_output, out
        return dlo_service_output, out

    def append_out(self, out, name, val, type):
        out["Variable_Name"].append(name)
        out["Variable_Value"].append(val)
        out["Variable_Data_Type"].append(type)
        return out

    def del_list_elements(self, list, position):
        del list[0][position]
        del list[1][position]

