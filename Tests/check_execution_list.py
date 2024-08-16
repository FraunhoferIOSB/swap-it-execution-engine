import unittest

from execution_engine_logic.service_execution.execution_dict import ServiceInfo, ExecutionList

class test_execution_list(unittest.TestCase):

    def test_add_service(self):
        test_val = "test"
        service_list = ExecutionList()
        #add a service
        service_list.add_service(ServiceInfo(test_val, test_val, False, test_val))
        self.assertEqual(service_list.services[0].service_name, test_val)
        self.assertEqual(service_list.services[0].service_uuid, test_val)
        self.assertEqual(service_list.services[0].task_uuid, test_val)
        self.assertEqual(service_list.services[0].completed, False)
        return service_list

    def test_set_service_finished(self):
        test_val = "test"
        service_list = self.test_add_service()
        res = service_list.set_service_to_completed(test_val, test_val)
        self.assertEqual(res, True)

    def test_remove_service(self):
        test_val = "test"
        service_list = self.test_add_service()
        service_list.remove_service()
        res = service_list.set_service_to_completed(test_val, test_val)
        self.assertEqual(res, True)
        service_uuid, task_uuid, service_name = service_list.remove_service()
        self.assertEqual(service_name, test_val)
        self.assertEqual(service_uuid, test_val)
        self.assertEqual(task_uuid, test_val)

if __name__ == "__main__":
    unittest.main()