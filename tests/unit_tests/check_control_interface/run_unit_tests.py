# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
import sys
sys.path.append("check_control_interface")
import time
import unittest, coverage
from .check_service_call import CheckServiceCall
from .check_target_server import CheckServerBrowsing
from .check_queue_interaction import QueueInteraction
from .check_default_assignment_agent import CheckAssignmentAgent
from .check_assignment import CheckAssignment
class RunControlInterfaceTests(unittest.TestCase):

    def run_control_interface_tests(self, cov =None, cusdtom_data_types = None):
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
            print("check_service_call")
            check_service_call = CheckServiceCall()
            check_service_call.run_check_service_call_from_literal(cov)
            check_service_call.run_check_service_call_from_data_object(cov)
            print("check_server_browsing")
            check_server_browsing = CheckServerBrowsing()
            check_server_browsing.run_test(cov)
            print("queue")
            queue = QueueInteraction()
            queue.run_queue_interaction(cov)
            time.sleep(3)
            print("check_default_assignment_agent")
            check_default_assignment_agent = CheckAssignmentAgent()
            check_default_assignment_agent.run_check_static_assignment(cov)
            check_default_assignment_agent.run_check_dynamic_assignment(cov)
            print("check_assignment")
            check_assignment = CheckAssignment()
            check_assignment.check_assignment(cov, cusdtom_data_types)
        cov.report()
        return cusdtom_data_types