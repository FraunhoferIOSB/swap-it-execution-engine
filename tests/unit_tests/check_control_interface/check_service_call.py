from tests.test_helpers.util.start_docker_compose import DockerComposeEnvironment
from tests.test_helpers.values.service_parameters import ServiceParameter
from control_interface.target_server.target_server_dict import TargetServerList
from control_interface.execute_service.check_service_in_and_output import CheckServiceMethodArguments
from control_interface.execute_service.interprete_result import ServiceResults
from control_interface.clients.event_subscription import ServiceEvents, SubHandler
import asyncio, unittest, time
from asyncua import Client, ua

ignore_files = "C:\Program Files\JetBrains\PyCharm 2024.1.3\plugins\python\helpers\pycharm\\"

class CheckServiceCall(unittest.TestCase):
    async def check_service_call_from_literal(self, cov):
        cov.start()
        env = DockerComposeEnvironment(["Service_Server"])
        env.run_docker_compose()
        time.sleep(10)
        service_browse_name = "GetPartsFromWarehouse"
        server_url = "opc.tcp://localhost:4081"
        iteration_time = 0.001
        # start client, connect to server and explore the server's namespace
        async with Client(url=server_url) as client:
            target_server_list = TargetServerList(None, iteration_time)
            target_server = await target_server_list.get_target_server(server_url, service_browse_name)
            target_server.Input_Arguments, target_server.Output_Arguments = await CheckServiceMethodArguments().browse_method_arguments(
                target_server.service_node, client, *await target_server.browse_result_data_type_nodes(client),
                target_server.event_node, service_browse_name,
                await target_server.load_custom_data_types(target_server.implementation, client))
            #get the service parameter
            param = ServiceParameter(target_server.client_custom_data_types)
            service_parameter = await target_server.match_service_input([["Literal"], [param.swap_order]], client,
                                                                        target_server.client_custom_data_types, service_browse_name)
            self.assertEqual(service_parameter[0], param.swap_order)
            await target_server.client_read_state_variable(client)
            #subscribe to the event
            handler = SubHandler(client, server_url, True)
            service_res = ServiceResults()
            if target_server.implementation == 'open62541':
                service_parameter = await service_res.create_input_variant(service_parameter)
            event_subscription = ServiceEvents(client, iteration_time, handler, target_server.event_node)
            event_node, event_filter = await event_subscription.subscribe_event_with_filter(service_browse_name, client)
            #check the event subscription with an eventfilter
            self.assertEqual(event_node.nodeid, ua.NodeId(NodeIdType=ua.NodeIdType.FourByte, NamespaceIndex=4, Identifier = 15001))
            self.assertEqual(event_filter, param.event_filter)
            await service_res.get_service_results(target_server, service_browse_name, service_parameter, handler,
                                                       client, target_server_list, event_subscription)
            self.assertEqual(service_res.result["SyncReturn"][0].ServiceResultMessage, param.service_results["SyncReturn"][0].ServiceResultMessage)
            self.assertEqual(service_res.result["SyncReturn"][0].ServiceResultCode, param.service_results["SyncReturn"][0].ServiceResultCode)
            self.assertEqual(service_res.result["SyncReturn"][0].ExpectedServiceExecutionDuration, param.service_results["SyncReturn"][0].ExpectedServiceExecutionDuration)
            self.assertEqual(service_res.result["AsyncReturn"][0].order_id, param.service_results["AsyncReturn"][0].order_id)
            #self.assertEqual(service_res.result["AsyncReturn"][0].stand, param.service_results["AsyncReturn"][0].stand)
            #self.assertEqual(service_res.result["AsyncReturn"][0].segments, param.service_results["AsyncReturn"][0].segments)
            self.assertEqual(service_res.result["AsyncReturn"][0].number_light_segments, param.service_results["AsyncReturn"][0].number_light_segments)
            await client.disconnect()
            env.stop_docker_compose()
            cov.stop()

    def run_check_service_call_from_data_object(self, cov):
        #todo
        print("not implemented yet")

    def run_check_service_call_from_literal(self, cov):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.check_service_call_from_literal(cov))

