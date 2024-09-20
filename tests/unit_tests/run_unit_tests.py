# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
import sys, os, unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "..\\..\\."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..\\..\\tests\\test_helpers\\."))
from check_control_interface.run_unit_tests import RunControlInterfaceTests
from check_execution_engine_logic.run_unit_tests import RunExecutionEngineLogicTests
from check_dispatcher.run_unit_tests import RunDispatcherTests


class ExecuteUnitTests(unittest.TestCase):

    def test_run_tests(self):
        custom_type_definitions = RunExecutionEngineLogicTests().run_execution_engine_logic_tests()
        custom_type_definitions = RunControlInterfaceTests().run_control_interface_tests(custom_type_definitions)
        custom_type_definitions = RunDispatcherTests().run_dispatcher_tests(custom_data_types = custom_type_definitions)


if __name__ == "__main__":
    unittest.main(exit=False)