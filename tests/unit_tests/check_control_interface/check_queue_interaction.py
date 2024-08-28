import unittest, asyncio, time, uuid
from tests.test_helpers.util.start_docker_compose import DockerComposeEnvironment
from tests.test_helpers.values.service_parameters import ServiceParameter
from control_interface.target_server.target_server_dict import TargetServerList
from control_interface.clients.queue_interaction import TargetServerQueue

from asyncua import Client

ignore_files = "C:\Program Files\JetBrains\PyCharm 2024.1.3\plugins\python\helpers\pycharm\\"

class QueueInteraction(unittest.TestCase):

    async def queue_interaction(self, cov):
        cov.start()
        env = DockerComposeEnvironment(["Service_Server"])
        env.run_docker_compose()
        time.sleep(10)

        service_browse_name = "GetPartsFromWarehouse"
        server_url = "opc.tcp://localhost:4081"
        iteration_time = 0.001
        # start client, connect to server and explore the server's namespace
        async with (Client(url=server_url) as client):
            target_server_list = TargetServerList(None, iteration_time)
            target_server = await target_server_list.get_target_server(server_url, service_browse_name)
            queue = TargetServerQueue(iteration_time, client)
            id_dict = Identifier()
            for i in range(3):
                id_dict.ids["Service"].append(str(uuid.uuid4()))
                id_dict.ids["Client"].append(await queue.client_add_queue_element(target_server, id_dict.ids["Service"][i]))
            #the queue elements are added asynchronously, so give the serter time to add them
            time.sleep(5)
            #check if the elements where added correctly
            value = await client.get_node(target_server.queue_variable).read_value()
            id_dict_new = Identifier()
            for i in range(len(value)):
                matched = False
                for j in range(len(id_dict.ids["Client"])):
                    if (str(value[i].Client_Identifier) == str(id_dict.ids["Client"][j])
                            and str(value[i].Service_UUID) == str(id_dict.ids["Service"][j])):
                        matched = True
                        id_dict_new.ids["Service"].append(id_dict.ids["Service"][j])
                        id_dict_new.ids["Client"].append(id_dict.ids["Client"][j])
                self.assertEqual(matched, True)
            #remove queue elements
            for i in range(len(value)):
                await queue.wait_for_queue_position_one(target_server, id_dict.ids["Client"][i], id_dict.ids["Service"][i])
                await queue.client_remove_queue_element(target_server, id_dict.ids["Service"][i], id_dict.ids["Client"][i])
            time.sleep(5)
            value = await client.get_node(target_server.queue_variable).read_value()
            param = ServiceParameter(target_server.client_custom_data_types)
            queue_type = param.get_custom_type("Queue_Data_Type")(Client_Identifier=None, Service_UUID=None, Entry_Number=param.get_custom_type("Queue_State_Variable_Type")(0), Queue_Element_State=0, ProductId=None, ServiceParameter=None)
            self.assertEqual(value, queue_type)
        env.stop_docker_compose()
        cov.stop()

    def run_queue_interaction(self, cov):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.queue_interaction(cov))

class Identifier:

    def __init__(self):
        self.ids = {"Client":[], "Service":[]}

