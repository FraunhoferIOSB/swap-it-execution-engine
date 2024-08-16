
class check_target_server:

    def __init__(self):
        self.passed = False

    def check_server(self, target_server):
        self.passed = True
        if target_server.service_node == None:
            self.passed = False
            print("target_server.service_node", target_server.service_node)
        if target_server.service_idx == None:
            self.passed = False
            print("target_server.service_idx", target_server.service_idx)
        if target_server.execution_node == None:
            self.passed = False
            print("target_server.service_execution_data_type_node", target_server.execution_node)
        if target_server.event_node == None:
            self.passed = False
            print("target_server.service_finished_event_type_node", target_server.event_node)
        if target_server.service_object == None:
            self.passed = False
            print("target_server.service_object", target_server.service_object)
        if target_server.state_variable == None:
            self.passed = False
            print("target_server.state_variable", target_server.state_variable)
        if target_server.queue_variable == None:
            self.passed = False
            print("target_server.queue_variable", target_server.queue_variable)
        if target_server.service_queue == None:
            self.passed = False
            print("target_server.service_queue", target_server.service_queue)
        if target_server.add_queue_element_bn == None:
            self.passed = False
            print("target_server.add_queue_element_bn", target_server.add_queue_element_bn)
        if target_server.remove_queue_element_bn == None:
            self.passed = False
            print("target_server.remove_queue_element_bn", target_server.remove_queue_element_bn)