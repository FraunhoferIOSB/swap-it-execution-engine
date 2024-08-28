import coverage, unittest, time
from tests.unit_tests.check_control_interface.run_unit_tests import RunControlInterfaceTests
from tests.unit_tests.check_execution_engine_logic.run_unit_tests import RunExecutionEngineLogicTests

ignore_files = "C:\\Program Files\\JetBrains\\PyCharm 2024.1.3\\plugins\\python\\helpers\\pycharm\\"

class ExecuteUnitTests(unittest.TestCase):

    def test_run_tests(self):
        print("run unit tests")
        cov = coverage.Coverage(cover_pylib=False,
                                omit=[ignore_files + "_jb_runner_tools.py",
                                      ignore_files + "_jb_serial_tree_manager.py",
                                      ignore_files + "teamcity\\common.py",
                                      ignore_files + "teamcity\\diff_tools.py",
                                      ignore_files + "teamcity\\messages.py",
                                      ignore_files + "teamcity\\unittestpy.py",
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
                                      "..\\test_helpers\\values\\ee_structures.py",
                                      "..\\test_helpers\\values\\service_parameters.py",
                                      ])

        with cov.collect():
            RunExecutionEngineLogicTests().run_execution_engine_logic_tests(cov)
            RunControlInterfaceTests().run_control_interface_tests(cov)





        #use to get files with annotated lines that indicate whether the line was executed or not
        #cov.annotate()
        cov.report()

if __name__ == "__main__":
    unittest.main()