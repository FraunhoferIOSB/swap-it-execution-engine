import coverage, unittest, asyncio, uuid
from asyncua import ua
from tests.test_helpers.values.ee_structures import DemoScenarioStructureTypes, DemoScenarioOPCUATypeInfo
from execution_engine_logic.execution_engine_server import ExecutionEngineServer
from execution_engine_logic.data_object.data_object_interaction import DataObject
from execution_engine_logic.data_types.internal_data_converter import EngineOpcUaDataConverter
from tests.test_helpers.util.server_explorer import CheckServerNamespace

ignore_files = "C:\Program Files\JetBrains\PyCharm 2024.1.3\plugins\python\helpers\pycharm\\"

class CheckExecutionEngineTypeGenerator(unittest.TestCase):

    async def generate_opcua_types(self, cov):
        cov.start()
        iteration_time = 0.001
        server_url = "opc.tcp://localhost:4001"
        server_instance = ExecutionEngineServer(execution_engine_server_url = server_url, log_info=True, iteration_time=iteration_time)
        await server_instance.init_server()
        types = DemoScenarioStructureTypes()
        type_info = DemoScenarioOPCUATypeInfo()
        structures = [types.swap_order, types.light_segment, types.stand_segment, types.raw_material, types.blank]
        server = await server_instance.start_server(structures, DataObject(EngineOpcUaDataConverter()))
        async with server:
            nodeIds = [ua.NodeId(Identifier=1, NamespaceIndex=0), ua.NodeId(Identifier=11, NamespaceIndex=0), ua.NodeId(Identifier=12, NamespaceIndex=0)]
            namespace = CheckServerNamespace(server_instance.idx)
            await namespace.start_client(server_url, server.nodes.types)
            for i in range(len(namespace.dataTypes)):
                node = await namespace.find_node_by_browsename(server.nodes.base_structure_type, namespace.dataTypes[i])
                nodeIds.append(node.nodeid)
            for i in range(len(namespace.dataTypes)):
                node = server.get_node(node)
                bn = await node.read_browse_name()
                curr_type = type_info.get_type_infor(str(bn.Name))
                td = await node.read_data_type_definition()
                for j in range(len(td.Fields)):
                    self.assertEqual(str(td.Fields[j].Name), str(curr_type[j].name))
                    self.assertEqual(td.Fields[j].ArrayDimensions, curr_type[j].arrayDim)
                    d_type_bn = await server.get_node(self.return_nodeId_infor(nodeIds, td.Fields[j].DataType)).read_browse_name()
                    self.assertEqual(str(d_type_bn.Name), str(curr_type[j].dataType))
            await server_instance.stop_server()
        cov.stop()
        print(server_instance.custom_data_types)
        return server_instance.custom_data_types
    def return_nodeId_infor(self, node_list, target_id):
        for i in range(len(node_list)):
            if(node_list[i].NamespaceIndex == target_id.NamespaceIndex and node_list[i].Identifier == target_id.Identifier):
                return node_list[i]
        return False

    def check_start_simple_server(self, cov):
        loop = asyncio.get_event_loop()
        types = loop.run_until_complete(self.generate_opcua_types(cov))
        return types



