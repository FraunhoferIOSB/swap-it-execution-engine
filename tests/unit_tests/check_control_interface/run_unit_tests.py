# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
import sys
sys.path.append("check_control_interface")
import time
import unittest
from .check_service_call import CheckServiceCall
from .check_target_server import CheckServerBrowsing
from .check_queue_interaction import QueueInteraction
from .check_default_assignment_agent import CheckAssignmentAgent
from .check_assignment import CheckAssignment
class RunControlInterfaceTests(unittest.TestCase):

    def run_control_interface_tests(self, custom_data_types = None, env = None):

        # run control_interface unit tests
        print("check_service_call")
        check_service_call = CheckServiceCall()
        check_service_call.run_check_service_call_from_literal(env = env)
        check_service_call.run_check_service_call_from_data_object()
        print("check_server_browsing")
        check_server_browsing = CheckServerBrowsing()
        check_server_browsing.run_test(env = env)
        print("queue")
        queue = QueueInteraction()
        queue.run_queue_interaction(env = env)
        time.sleep(3)
        print("check_default_assignment_agent")
        check_default_assignment_agent = CheckAssignmentAgent()
        check_default_assignment_agent.run_check_static_assignment(env = env)
        check_default_assignment_agent.run_check_dynamic_assignment(env = env)
        print("check_assignment", custom_data_types)
        check_assignment = CheckAssignment()
        check_assignment.check_assignment(custom_data_types, env = env)
        return custom_data_types