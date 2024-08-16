# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from asyncua import ua
from datetime import datetime


class ServiceResults:

    def __init__(self):
        self.result = {"SyncReturn": [], "AsyncReturn": []}

    def transmit_service_execution_finished(self, service_uuid, task_uuid, service_execution_list):
        if(service_execution_list.set_service_to_completed(service_uuid, task_uuid) == False):
            print("[ ", datetime.now(), " ] ERROR during execution, Executed service is not in the service_execution_list")
        return service_execution_list

    async def get_service_results(self, target_server, service_browse_name, service_parameter, handler, client, target_server_list, event_subscription):
        method_node = client.get_node(target_server.service_object)
        if target_server.Output_Arguments["OutputArgumentType"] == target_server_list.async_result:
            await event_subscription.subscribe_event_with_filter(service_browse_name, client)
            sync_result = await method_node.call_method(str(target_server.service_idx) + ":" + str(service_browse_name), *service_parameter)
            if sync_result:
                self.result["SyncReturn"].append(sync_result)
            async_result = await event_subscription.wait_event_results(handler)
            if async_result:
                for i in range(len(async_result)):
                    self.result["AsyncReturn"].append(async_result[i])
        else:
            self.result["SyncReturn"].append(await method_node.call_method(
                str(target_server.service_idx) + ":" + str(service_browse_name), *service_parameter))

    async def create_input_variant(self, service_parameter):
        for i in range(len(service_parameter)):
            service_parameter[i] = ua.Variant(service_parameter[i], ua.VariantType.ExtensionObject)
        return service_parameter

    async def add_result_to_the_data_lifecycle_object(self, target_server, dlo_service_output, task_uuid, service_uuid, client_custom_data_types, name):
        results_for_dlo = await target_server.service_arguments.extract_service_output(target_server.Output_Arguments, self.result, dlo_service_output, client_custom_data_types)
        await target_server.append_service_results(task_uuid, service_uuid, results_for_dlo, name)
