# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import sys
sys.path.append("check_execution_engine_logic")
import unittest
from .check_execution_list import CheckExecutionList
from .check_execution_engine_server import CheckExecutionEngineServer
from .check_opcua_type_generator import CheckExecutionEngineTypeGenerator
from .check_data_converter import CheckInternalDataConverter
class RunExecutionEngineLogicTests(unittest.TestCase):
    def run_execution_engine_logic_tests(self,custom_type_definitions = None):
        print("check_type_generator")
        check_type_generator = CheckExecutionEngineTypeGenerator()
        custom_type_definitions = check_type_generator.check_start_simple_server()
        print("check_execution_list")
        check_execution_list = CheckExecutionList()
        check_execution_list.run_tests()
        print("check_execution_engine_server")
        check_execution_engine_server = CheckExecutionEngineServer()
        check_execution_engine_server.check_start_simple_server()
        print("check_data_converter")
        check_data_converter = CheckInternalDataConverter()
        custom_type_definitions = check_data_converter.check_start_simple_server(custom_type_definitions)
        return custom_type_definitions
