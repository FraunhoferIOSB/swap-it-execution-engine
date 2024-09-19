# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import unittest, coverage
from tests.unit_tests.check_execution_engine_logic.check_execution_list import CheckExecutionList
from tests.unit_tests.check_execution_engine_logic.check_execution_engine_server import CheckExecutionEngineServer
from tests.unit_tests.check_execution_engine_logic.check_opcua_type_generator import CheckExecutionEngineTypeGenerator
from tests.unit_tests.check_execution_engine_logic.check_data_converter import CheckInternalDataConverter
class RunExecutionEngineLogicTests(unittest.TestCase):

    def run_execution_engine_logic_tests(self, cov = None, custom_type_definitions = None):
        if cov == None:
            cov = coverage.Coverage(cover_pylib=False,
                                omit=[
                                      "check_execution_engine_server.py",
                                      "check_execution_list.py",
                                      "check_opcua_type_generator.py",
                                      "check_control_interface\\check_default_assignment_agent.py",
                                      "check_control_interface\\check_queue_interaction.py",
                                      "check_control_interface\\check_service_call.py",
                                      "check_control_interface\\check_target_server.py",
                                      "check_control_interface\\run_unit_tests.py",
                                      "check_execution_engine_logic\\check_data_converter.py",
                                      "check_execution_engine_logic\\run_unit_tests.py",
                                      "check_dispatcher\\check_service_input_filtering.py",
                                      "..\\test_helpers\\util\\server_explorer.py",
                                      "..\\test_helpers\\util\\start_docker_compose.py",
                                      "..\\test_helpers\\values\\ee_structures.py",
                                      "..\\test_helpers\\values\\service_parameters.py",
                                      "..\\test_helpers\\util\\execution_engine_server.py",
                                      ])

        with cov.collect():
            print("check_type_generator")
            check_type_generator = CheckExecutionEngineTypeGenerator()
            custom_type_definitions = check_type_generator.check_start_simple_server(cov)
            check_execution_list = CheckExecutionList()
            check_execution_list.run_tests(cov)
            print("check_execution_engine_server")
            check_execution_engine_server = CheckExecutionEngineServer()
            check_execution_engine_server.check_start_simple_server(cov)
            print("check_data_converter", custom_type_definitions)
            check_data_converter = CheckInternalDataConverter()
            custom_type_definitions = check_data_converter.check_start_simple_server(cov, custom_type_definitions)
        cov.report()
        return custom_type_definitions
