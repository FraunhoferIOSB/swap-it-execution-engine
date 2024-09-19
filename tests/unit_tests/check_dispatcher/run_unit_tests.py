# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import sys
sys.path.append("check_dispatcher")

import unittest, coverage
from check_task_started_callbacks import CheckTaskStartedDispatcherCallback
from check_task_finished_callback import CheckTaskFinishedDispatcherCallback
from check_data_callbacks import CheckDataDispatcherCallback
from check_service_callbacks import CheckServiceStartedDispatcherCallback
from check_service_input_filtering import CheckServiceStartedInputFiltering


class RunDispatcherTests(unittest.TestCase):

    def run_dispatcher_tests(self, cov = None, custom_data_types = None):
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
                                      "..\\test_helpers\\util\\server_explorer.py",
                                      "..\\test_helpers\\util\\start_docker_compose.py",
                                      "..\\test_helpers\\util\\execution_engine_server.py",
                                      "..\\test_helpers\\values\\ee_structures.py",
                                      "..\\test_helpers\\values\\service_parameters.py",
                                      ])
        with cov.collect():
            # run control_interface unit tests
            print("task started")
            check_task_started_dispatcher_callabcks = CheckTaskStartedDispatcherCallback()
            custom_data_types = check_task_started_dispatcher_callabcks.check_task_started_callbacks_test(cov = cov, custom_data_types=custom_data_types)
            print("task finished")
            check_task_finished_dispatcher_callabcks = CheckTaskFinishedDispatcherCallback()
            custom_data_types = check_task_finished_dispatcher_callabcks.check_task_finished_callbacks_test(cov = cov, custom_data_types=custom_data_types)
            print("data callback")
            check_data_dispatcher_callback = CheckDataDispatcherCallback()
            custom_data_types = check_data_dispatcher_callback.check_data_callbacks_test(cov = cov, custom_data_types=custom_data_types)
            print("service started")
            check_service_started_dispatcher_callback = CheckServiceStartedDispatcherCallback()
            custom_data_types = check_service_started_dispatcher_callback.check_service_started_callbacks_test_without_tasks(cov = cov, custom_data_types=custom_data_types)
            custom_data_types = check_service_started_dispatcher_callback.check_service_started_callbacks_test_with_tasks(cov = cov, custom_data_types=custom_data_types)
            print("service started input filtering")
            check_service_input_filtering_test = CheckServiceStartedInputFiltering()
            custom_data_types = check_service_input_filtering_test.run_test(cov = cov, custom_data_types=custom_data_types)

        cov.report()
        return custom_data_types

#if __name__ == "__main__":
#    unittest.main()