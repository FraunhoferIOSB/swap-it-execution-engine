# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

from asyncua import ua, Server
from asyncua.common.structures104 import new_struct, new_struct_field

class ExtractPFDL:
    def distinguish_between_struct_and_array(self, element, variable_types, array_length, referred_struct):
        self.element = element
        self.variable_types = variable_types
        self.array_length = array_length
        self.referred_struct = referred_struct
        conv_to_str = str(self.element)
        if conv_to_str[len(conv_to_str) - 1] != ']':
            self.variable_types.append("Struct"), self.array_length.append('None'), self.referred_struct.append(conv_to_str)
        for x in range(len(conv_to_str) - 1):
            if conv_to_str[x] == '[' and conv_to_str[x + 1] == ']':
                if conv_to_str[:len(conv_to_str) - 2] == 'number':
                    self.variable_types.append("Double"), self.array_length.append("Unspecific"), self.referred_struct.append(None)
                elif conv_to_str[:len(conv_to_str) - 2] == 'string':
                    self.variable_types.append("String"), self.array_length.append("Unspecific"), self.referred_struct.append(None)
                elif conv_to_str[:len(conv_to_str) - 2] == 'boolean':
                    self.variable_types.append("Boolean"), self.array_length.append("Unspecific"), self.referred_struct.append(None)
                else:
                    self.variable_types.append("Struct"), self.array_length.append('Unspecific'), self.referred_struct.append(conv_to_str[0:x])
            elif conv_to_str[x] == '[' and conv_to_str[x + 1] != ']':
                ctr = 0
                str_name = ''
                while conv_to_str[ctr] != '[':
                    str_name = str_name + conv_to_str[ctr]
                    ctr += 1
                if str_name == 'number':
                    self.variable_types.append("Double")
                elif str_name == 'string':
                    self.variable_types.append("String")
                elif str_name == 'boolean':
                    self.variable_types.append("Boolean")
                self.array_length.append(conv_to_str[x + 1]), self.referred_struct.append(None)
            else:
                pass
        return self.variable_types, self.array_length, self.referred_struct

    def create_struct_dict(self, pfdl_structs):
        self.pfdl_structs = pfdl_structs
        self.struct_dictionary = {"Struct": [], "Variable_Name": [], "Variable_Type": [], "Array_Length": [], "Referred_Struct": []}
        structs = dict()
        structs['structs'] = self.pfdl_structs
        for attributes in structs.values():
            for struct in attributes.values():
                for (header, val) in struct.__dict__.items():
                    variable_names, variable_types, array_length, referred_struct = [], [], [], []
                    # append the corresponding values to the struct_dictionary
                    if header == 'name':
                        self.struct_dictionary["Struct"].append(val)
                    if header == 'attributes':
                        for variable_name, variable_type in struct.__dict__[header].items():
                            variable_names.append(variable_name)
                            if variable_type == "string":
                                variable_types.append("String"), array_length.append(None), referred_struct.append(None)
                            elif variable_type == "number":
                                variable_types.append("Double"), array_length.append(None), referred_struct.append(None)
                            elif variable_type == "boolean":
                                variable_types.append("Boolean"), array_length.append(None), referred_struct.append(None)
                            else:
                                variable_types, array_length, referred_struct = self.distinguish_between_struct_and_array(variable_type, variable_types, array_length, referred_struct)
                        self.struct_dictionary["Variable_Name"].append(variable_names)
                        self.struct_dictionary["Variable_Type"].append(variable_types)
                        self.struct_dictionary["Array_Length"].append(array_length)
                        self.struct_dictionary["Referred_Struct"].append(referred_struct)
        return self.struct_dictionary

class GeneratePfdlTypes:

    def __init__(self, server, idx):
        self.server = server
        self.idx = idx

    async def create_parameter_struct_data_types(self, struct_overview):
        struct_overview = await self.order_struct_overview(struct_overview)
        appended_data_types = {"Name": [], "Struct_Node_Id": []}
        for i in range(len(struct_overview["Struct"])):
            struct_fields = []
            for j in range(len(struct_overview["Variable_Name"][i])):
                Is_Array = False if str(struct_overview["Array_Length"][i][j]) == "None" else True
                data_type = []
                if str(struct_overview["Referred_Struct"][i][j]) == "None":
                    data_type.append(ua.VariantType(ua.VariantType[struct_overview["Variable_Type"][i][j]].value))
                else:
                    for k in range(len(appended_data_types["Name"])):
                        if appended_data_types["Name"][k] == struct_overview["Referred_Struct"][i][j]:
                            data_type.append(appended_data_types["Struct_Node_Id"][k])
                field = new_struct_field(struct_overview["Variable_Name"][i][j], data_type[0], array=Is_Array)
                struct_fields.append(field)
            new_structure_node, _ = await new_struct(self.server, self.idx, struct_overview["Struct"][i],[*struct_fields])
            appended_data_types["Name"].append(struct_overview["Struct"][i]), appended_data_types["Struct_Node_Id"].append(new_structure_node)

    async def order_struct_overview(self, struct_overview):
        ordered_struct_overview = {"Struct":[], "Variable_Name":[], "Variable_Type":[], "Array_Length":[], "Referred_Struct":[]}
        struct_ctr = 0
        number_of_structs = len(struct_overview["Struct"])
        while len(struct_overview["Struct"])>0:
            # stop the program if an referred struct does not exist
            if struct_ctr > number_of_structs:
                print("Unsolved reference to struct, check PFDL file")
            else:
                for i in range(len(struct_overview["Struct"])):
                    #indicates for each struct element if it is an struct
                    self.missing_required_reference = []
                    for item in struct_overview["Referred_Struct"][i]:
                        if item != None:
                            self.struct_not_found = True
                            #case 1: the referred struct is already on the ordered list -> the struct can be added self.struct_found becomes True
                            for struct in ordered_struct_overview["Struct"]:
                                if item == struct:
                                    self.struct_not_found = False
                                    break
                            # case 2: the referred struct is not on the ordered list -> struct must be skipped self.struct_found stays false
                            self.missing_required_reference.append(self.struct_not_found)
                        else:
                            self.missing_required_reference.append(False)
                    # check if all required structs exist -> if so append the struct to the ordered list, else the loop continiues with the next
                    if not any(self.missing_required_reference):
                        struct = {"Struct": [struct_overview["Struct"][i]],
                                  "Variable_Name":[struct_overview["Variable_Name"][i]],
                                  "Variable_Type":[struct_overview["Variable_Type"][i]],
                                  "Array_Length":[struct_overview["Array_Length"][i]],
                                  "Referred_Struct":[struct_overview["Referred_Struct"][i]]}
                        ordered_struct_overview = await self.add_struct_to_ordered_list(ordered_struct_overview, struct)
                        await self.remove_struct_from_overview(struct_overview,i)
                        struct_ctr += 1
                        break
        return ordered_struct_overview

    async def remove_struct_from_overview(self, struct, ctr):
        key_list = ["Struct", "Variable_Name", "Variable_Type", "Array_Length", "Referred_Struct"]
        for i in key_list:
            del struct[i][ctr]

    async def add_struct_to_ordered_list(self, ordered_struct_overview, struct):
        for (key, value) in struct.items():
            ordered_struct_overview[key].append(value[0])
        return ordered_struct_overview





