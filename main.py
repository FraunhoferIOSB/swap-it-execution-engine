import asyncio
from execution_engine_logic.execution_engine import ExecutionEngine
from dispatcher.dispatcher_configuration import PfdlDispatcherConfig

pfdl_directory = "./PFDL_Examples/"
pfdl_file_name = ["patient_zero.pfdl"]
global path_to_pfdl
path_to_pfdl = pfdl_directory + pfdl_file_name[0]

#set up iteration time
iteration_time = 0.00001
number_default_clients = 5

device_registry_url = "opc.tcp://localhost:8000"
execution_engine_server_url = "opc.tcp://localhost:4000"


#docker
#device_registry_url = "opc.tcp://host.docker.internal:8000"
#device_registry_url = "opc.tcp://device_registry:8000"
#execution_engine_server_url = "opc.tcp://execution_engine:4000"
#dashboard_host_address = "http://dashboard:8080"




assignment_agent_url = None
service_tracking = True
delay_start = None

if __name__ == "__main__":
    dispatcher = PfdlDispatcherConfig(path_to_pfdl)
    dispatcher.config_dispatcher()


    main_loop = asyncio.new_event_loop()
    main_loop.run_until_complete(ExecutionEngine(
                         execution_engine_server_url,
                         iteration_time,
                         service_tracking,
                         number_default_clients,
                         device_registry_url,
                         assignment_agent_url,
                         dispatcher.dispatcher_object,
                         delay_start
                         ).main())

