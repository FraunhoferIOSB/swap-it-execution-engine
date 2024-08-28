from Dispatcher.dispatcher_callbacks.callback_helpers import callback_helpers
from ControlInterface.target_server.target_server_dict import target_server_list
from execution_engine_logic.service_execution.execution_dict import ServiceInfo, ExecutionList
import asyncio
import nest_asyncio
from datetime import datetime


class DispatcherTestCallbackFunctions:
    def __init__(self, server_instance: object, server: object, read_pfdl: object, execution_engine: object) -> object:
        self.server = server
        self.server_instance = server_instance
        self.read_pfdl = read_pfdl
        self.callback_helpers = callback_helpers(self.server, self.read_pfdl)



    # task_finished_cb
    def task_finished_cb(self, name:str, task_identifier, context:str, output_parameters):
        print("Task finished")

    #start task callback
    def task_started_cb(self, name:str, task_identifier, context:str, input_parameters, input_parameters_instances, running, dispatcher_object):
        print("Task started")
        if name != "productionTask":
            print(input_parameters_instances)
            #task_input_type = self.callback_helpers.distinguish_struct_and_literal_input(input_parameters_instances)
            #print(task_input_type)
        #terminate scheduler
        dispatcher_object.running = running

    #def service_started_cb(self, service: Service):
    def service_started_cb(self, name, service_identifier, context, input_parameters, output_parameters):
        print("service started")


    #service_finished_cb
    def service_finished_cb(self, name, service_identifier, context):
        print("service finished")