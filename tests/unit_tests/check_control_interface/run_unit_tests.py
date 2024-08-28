import unittest
from tests.unit_tests.check_control_interface.check_service_call import CheckServiceCall
from tests.unit_tests.check_control_interface.check_target_server import CheckServerBrowsing
from tests.unit_tests.check_control_interface.check_queue_interaction import QueueInteraction
from tests.unit_tests.check_control_interface.check_default_assignment_agent import CheckAssignmentAgent

class RunControlInterfaceTests(unittest.TestCase):
    def run_control_interface_tests(self, cov):
        with cov.collect():
            # run control_interface unit tests
            check_service_call = CheckServiceCall()
            check_service_call.run_check_service_call_from_literal(cov)
            check_service_call.run_check_service_call_from_data_object(cov)
            check_server_browsing = CheckServerBrowsing()
            check_server_browsing.run_test(cov)
            queue = QueueInteraction()
            queue.run_queue_interaction(cov)
            check_default_assignment_agent = CheckAssignmentAgent()
            check_default_assignment_agent.run_check_static_assignment(cov)
            check_default_assignment_agent.run_check_dynamic_assignment(cov)