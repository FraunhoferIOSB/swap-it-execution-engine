# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import sys
sys.path.append("check_dispatcher")
import unittest
from .check_task_started_callbacks import CheckTaskStartedDispatcherCallback
from .check_task_finished_callback import CheckTaskFinishedDispatcherCallback
from .check_data_callbacks import CheckDataDispatcherCallback
from .check_service_callbacks import CheckServiceStartedDispatcherCallback
from .check_service_input_filtering import CheckServiceStartedInputFiltering


class RunDispatcherTests(unittest.TestCase):

    def run_dispatcher_tests(self, custom_data_types = None, env = None):
            # run control_interface unit tests
            print("task started")
            check_task_started_dispatcher_callabcks = CheckTaskStartedDispatcherCallback()
            custom_data_types = check_task_started_dispatcher_callabcks.check_task_started_callbacks_test(custom_data_types=custom_data_types, env = env)
            print("task finished")
            check_task_finished_dispatcher_callabcks = CheckTaskFinishedDispatcherCallback()
            custom_data_types = check_task_finished_dispatcher_callabcks.check_task_finished_callbacks_test(custom_data_types=custom_data_types, env = env)
            print("data callback")
            check_data_dispatcher_callback = CheckDataDispatcherCallback()
            custom_data_types = check_data_dispatcher_callback.check_data_callbacks_test(custom_data_types=custom_data_types, env = env)
            print("service started")
            check_service_started_dispatcher_callback = CheckServiceStartedDispatcherCallback()
            custom_data_types = check_service_started_dispatcher_callback.check_service_started_callbacks_test_without_tasks(custom_data_types=custom_data_types, env = env)
            custom_data_types = check_service_started_dispatcher_callback.check_service_started_callbacks_test_with_tasks(custom_data_types=custom_data_types, env = env)
            print("service started input filtering")
            check_service_input_filtering_test = CheckServiceStartedInputFiltering()
            custom_data_types = check_service_input_filtering_test.run_test(custom_data_types=custom_data_types, env = env)
            return custom_data_types
