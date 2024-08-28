# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
import unittest, coverage, asyncio, time
from tests.test_helpers.util.start_docker_compose import DockerComposeEnvironment

ignore_files = "C:\Program Files\JetBrains\PyCharm 2024.1.3\plugins\python\helpers\pycharm\\"

class CheckControlInterface(unittest.TestCase):

    async def check_static_assignment(self):
        #todo write the test
        cov = coverage.Coverage()
        cov.start()
        env = DockerComposeEnvironment(["Service_Server", "Device_Registry"])
        env.run_docker_compose()
        time.sleep(10)
        service_browse_name = "GetPartsFromWarehouse"
        server_url = "opc.tcp://localhost:4081"
        iteration_time = 0.001



        env.stop_docker_compose()
        cov.stop()
        cov.report(omit=[ignore_files + "_jb_runner_tools.py",
                         ignore_files + "_jb_serial_tree_manager.py",
                         ignore_files + "teamcity\common.py",
                         ignore_files + "teamcity\diff_tools.py",
                         ignore_files + "teamcity\messages.py",
                         ignore_files + "teamcity\\unittestpy.py",
                         "..\\docker_environment\\start_docker_compose.py"
                         ])


    def test_check_assignment(self, cov):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.check_static_assignment(cov))





if __name__ == "__main__":
    unittest.main()