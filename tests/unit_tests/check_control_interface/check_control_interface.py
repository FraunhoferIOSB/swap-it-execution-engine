# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
import unittest, asyncio, time
from util.start_docker_compose import DockerComposeEnvironment

ignore_files = "C:\Program Files\JetBrains\PyCharm 2024.1.3\plugins\python\helpers\pycharm\\"

class CheckControlInterface(unittest.TestCase):

    async def check_static_assignment(self):
        #todo write the test
        env = DockerComposeEnvironment(["Device_Registry", "Service_Server"])
        env.run_docker_compose()
        time.sleep(10)
        service_browse_name = "GetPartsFromWarehouse"
        server_url = "opc.tcp://localhost:4081"
        iteration_time = 0.001
        env.stop_docker_compose()

    def test_check_assignment(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.check_static_assignment())

if __name__ == "__main__":
    unittest.main()