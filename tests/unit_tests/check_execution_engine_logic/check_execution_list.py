# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

import unittest
from execution_engine_logic.service_execution.execution_dict import ServiceInfo, ExecutionList

class CheckExecutionList(unittest.TestCase):

    def run_tests(self):
        test_val = "test"
        service_list = ExecutionList()
        # add a service
        service_list.add_service(ServiceInfo(test_val, test_val, False, test_val))
        self.assertEqual(service_list.services[0].service_name, test_val)
        self.assertEqual(service_list.services[0].service_uuid, test_val)
        self.assertEqual(service_list.services[0].task_uuid, test_val)
        self.assertEqual(service_list.services[0].completed, False)
        res = service_list.set_service_to_completed(test_val, test_val)
        self.assertEqual(res, True)
        #remove a service
        test_val = "test"
        service_list = ExecutionList()
        service_list.add_service(ServiceInfo(test_val, test_val, False, test_val))
        self.assertEqual(service_list.services[0].service_name, test_val)
        self.assertEqual(service_list.services[0].service_uuid, test_val)
        self.assertEqual(service_list.services[0].task_uuid, test_val)
        self.assertEqual(service_list.services[0].completed, False)
        service_list.remove_service()
        res = service_list.set_service_to_completed(test_val, test_val)
        self.assertEqual(res, True)
        service_uuid, task_uuid, service_name = service_list.remove_service()
        self.assertEqual(service_name, test_val)
        self.assertEqual(service_uuid, test_val)
        self.assertEqual(task_uuid, test_val)