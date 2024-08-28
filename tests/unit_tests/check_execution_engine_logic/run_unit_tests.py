import unittest
from tests.unit_tests.check_execution_engine_logic.check_execution_list import CheckExecutionList
from tests.unit_tests.check_execution_engine_logic.check_execution_engine_server import CheckExecutionEngineServer
from tests.unit_tests.check_execution_engine_logic.check_opcua_type_generator import CheckExecutionEngineTypeGenerator
from tests.unit_tests.check_execution_engine_logic.check_data_converter import CheckInternalDataConverter

class RunExecutionEngineLogicTests(unittest.TestCase):
    def run_execution_engine_logic_tests(self, cov):
        with cov.collect():
            print("check_type_generator")
            check_type_generator = CheckExecutionEngineTypeGenerator()
            custom_type_definitions = check_type_generator.check_start_simple_server(cov)
            check_execution_list = CheckExecutionList()
            check_execution_list.run_tests(cov)
            print("check_execution_engine_server")
            check_execution_engine_server = CheckExecutionEngineServer()
            check_execution_engine_server.check_start_simple_server(cov)
            print("check_data_converter")
            check_data_converter = CheckInternalDataConverter()
            check_data_converter.check_start_simple_server(cov, custom_type_definitions)

