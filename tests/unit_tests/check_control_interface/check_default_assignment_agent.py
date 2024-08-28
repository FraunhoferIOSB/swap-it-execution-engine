import unittest, asyncio, time, uuid
from asyncua import Client
from tests.test_helpers.util.start_docker_compose import DockerComposeEnvironment
from control_interface.target_server.target_server_dict import TargetServerList
from control_interface.execute_service.default_assignment_agent import DefaultAssignmentAgent
from control_interface.execute_service.assign_agent import AssignAgent
from control_interface.clients.queue_interaction import TargetServerQueue

class CheckAssignmentAgent(unittest.TestCase):
    #assign to single resource
    async def check_static_assignment(self, cov):
        cov.start()
        env = DockerComposeEnvironment(["Device_Registry", "Service_Server"])
        env.run_docker_compose()
        time.sleep(10)
        service_browse_name = "Gluing"
        server_url = "opc.tcp://localhost:8000"
        filter_agent_input = [service_browse_name, ["None"], ["None"]]
        a_agent = AssignAgent(True)
        async with Client(url=server_url) as client:
            agent_list = await a_agent.get_agents_from_the_device_registry(client, filter_agent_input)
            await client.disconnect()
        self.assertIsNot(None, agent_list)
        target_agent = await DefaultAssignmentAgent(server_url, agent_list).find_target_resource()
        self.assertEqual(str(target_agent), "opc.tcp://host.docker.internal:4061")
        env.stop_docker_compose()
        cov.stop()
    #from multiple resources
    async def check_dynamic_assignment(self, cov):
        cov.start()
        env = DockerComposeEnvironment(["Device_Registry", "Service_Server"])
        env.run_docker_compose()
        time.sleep(10)
        service_browse_name = "GetPartsFromWarehouse"
        server_url = "opc.tcp://localhost:8000"
        target_server_list = ["opc.tcp://localhost:4081", "opc.tcp://localhost:4082"]
        iteration_time = 0.001
        filter_agent_input = [service_browse_name, ["None"], ["None"]]
        a_agent = AssignAgent(True)
        async with Client(url=server_url) as client:
            agent_list = await a_agent.get_agents_from_the_device_registry(client, filter_agent_input)
            await client.disconnect()
        self.assertIsNot(None, agent_list)
        #add some queue elements to both target server
        elements = [2, 3]
        client_ids, service_ids = [], []
        for i, j in zip(elements, target_server_list):
            for z in range(i):
                async with Client(url=j) as client:
                    t_server_list = TargetServerList(None, iteration_time)
                    target_server = await t_server_list.get_target_server(j, service_browse_name)
                    queue = TargetServerQueue(iteration_time, client)
                    service_uuid = str(uuid.uuid4())
                    service_ids.append(service_uuid)
                    client_id = await queue.client_add_queue_element(target_server, service_uuid)
                    client_ids.append(client_id)
                    await client.disconnect()
        time.sleep(3)
        #now check the assignment, opc.tcp://localhost:4081 should be assigned, since it has only 2 elements
        target_agent = await DefaultAssignmentAgent(server_url, agent_list).find_target_resource()
        self.assertEqual(str(a_agent.convert_url_from_docker(target_agent)), target_server_list[0])
        #next, remove the elements from server opc.tcp://localhost:4082 and re-assign
        async with Client(url=target_server_list[1]) as client:
            for i in range(elements[1]):
                queue = TargetServerQueue(iteration_time, client)
                target_server = await t_server_list.get_target_server(target_server_list[1], service_browse_name)
                await queue.client_remove_queue_element(target_server, service_ids[i+2], client_ids[i+2])
            await client.disconnect()
        time.sleep(3)
        target_agent = await DefaultAssignmentAgent(server_url, agent_list).find_target_resource()
        self.assertEqual(str(a_agent.convert_url_from_docker(target_agent)), target_server_list[1])
        env.stop_docker_compose()
        cov.stop()

    def run_check_static_assignment(self, cov):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.check_static_assignment(cov))

    def run_check_dynamic_assignment(self, cov):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.check_dynamic_assignment(cov))

if __name__ == "__main__":
    unittest.main()