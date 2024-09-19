# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import coverage, unittest
from tests.unit_tests.check_control_interface.run_unit_tests import RunControlInterfaceTests
from tests.unit_tests.check_execution_engine_logic.run_unit_tests import RunExecutionEngineLogicTests
from tests.unit_tests.check_dispatcher.run_unit_tests import RunDispatcherTests


class ExecuteUnitTests(unittest.TestCase):

    def test_run_tests(self):
        print("run unit tests")
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
                                      "check_control_interface\\check_assignment.py",
                                      "check_execution_engine_logic\\check_data_converter.py",
                                      "check_execution_engine_logic\\run_unit_tests.py",
                                      "check_dispatcher\\check_task_started_callbacks.py",
                                      "check_dispatcher\\run_unit_tests.py",
                                      "check_dispatcher\\check_data_callbacks.py",
                                      "check_dispatcher\\check_task_finished_callback.py",
                                      "check_dispatcher\\check_service_callbacks.py",
                                      "check_dispatcher\\execution_engine_server.py",
                                      "check_dispatcher\\check_service_input_filtering.py",
                                      "..\\test_helpers\\util\\server_explorer.py",
                                      "..\\test_helpers\\util\\execution_engine_server.py",
                                      "..\\test_helpers\\util\\start_docker_compose.py",
                                      "..\\test_helpers\\util\\observer_client.py",
                                      "..\\test_helpers\\values\\ee_structures.py",
                                      "..\\test_helpers\\values\\service_parameters.py",
                                      ])
        with cov.collect():
            custom_type_definitions = RunExecutionEngineLogicTests().run_execution_engine_logic_tests(cov)
            custom_type_definitions = RunControlInterfaceTests().run_control_interface_tests(cov, custom_type_definitions)
            custom_type_definitions = RunDispatcherTests().run_dispatcher_tests(cov, custom_type_definitions)
        cov.report()

if __name__ == "__main__":
    unittest.main()