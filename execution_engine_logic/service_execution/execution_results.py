# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

class ExecutionParameter():

    def __init__(self, service_uuid: str, context: str, service_results: [], output_variables: [], output_variable_type: [], name: str):
        self.service_uuid = service_uuid
        self.context = context
        self.results = service_results
        self.variables = output_variables
        self.type = output_variable_type
        self.name = name

class ExecutionParameterList:

    def __init__(self):
        self.parameters = []

    def add_parameter(self, parameter: ExecutionParameter):
        self.parameters.append(parameter)

    def remove_parameter(self, service_uuid):
        for i in range(len(self.parameters)-1, -1, -1):
            if str(self.parameters[i].service_uuid) == str(service_uuid):
                del self.parameters[i]
                return



