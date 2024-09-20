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

    def run_control_interface_tests(self, cusdtom_data_types = None):

        # run control_interface unit tests
        print("check_service_call")
        check_service_call = CheckServiceCall()
        check_service_call.run_check_service_call_from_literal()
        check_service_call.run_check_service_call_from_data_object()
        print("check_server_browsing")
        check_server_browsing = CheckServerBrowsing()
        check_server_browsing.run_test()
        print("queue")
        queue = QueueInteraction()
        queue.run_queue_interaction()
        time.sleep(3)
        print("check_default_assignment_agent")
        check_default_assignment_agent = CheckAssignmentAgent()
        check_default_assignment_agent.run_check_static_assignment()
        check_default_assignment_agent.run_check_dynamic_assignment()
        print("check_assignment")
        check_assignment = CheckAssignment()
        check_assignment.check_assignment(cusdtom_data_types)
        return cusdtom_data_types