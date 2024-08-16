# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
class EngineStruct:

    def __init__(self, name):
        self.name: str = name
        self.attributes = {}
        self.data_type = None

    def add_attribute(self, name, value):
        self.attributes[name] = value

    def set_struct_type(self, type):
        self.data_type = type

class EngineArray:

    def __init__(self, name, length):
        self.name = name
        self.data_type = None
        self.length = length
        self.values = []

    def set_array_type(self, type):
        self.data_type = type

    def add_value(self, value):
        self.values.append(value)
