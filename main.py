import asyncio
from execution_engine_logic.execution_engine import ExecutionEngine
from dispatcher.dispatcher_configuration import DispatcherConfig



pfdl_directory = "./PFDL_Examples/"
#pfdl_file_name = ["advanced.pfdl"]
#pfdl_file_name = ["advanced.pfdl"]
pfdl_file_name = ["patient_zero.pfdl"]

#pfdl_directory = "./Tutorial/PFDl/"
#pfdl_file_name = ["dynamic.pfdl"]

path_to_pfdl = pfdl_directory + pfdl_file_name[0]

#docker
#device_registry_url = "opc.tcp://host.docker.internal:8000"
#device_registry_url = "opc.tcp://device_registry:8000"
#execution_engine_server_url = "opc.tcp://execution_engine:4000"
#dashboard_host_address = "http://dashboard:8080"

number_default_clients = 5
device_registry_url = "opc.tcp://localhost:8000"
execution_engine_server_url = "opc.tcp://localhost:4000"
dashboard = "http://localhost:8080"

service_tracking = True
docker = True

if __name__ == "__main__":

    main_loop = asyncio.new_event_loop()
    main_loop.run_until_complete(ExecutionEngine(
                         server_url=execution_engine_server_url,
                         dispatcher_object=DispatcherConfig(filepath=path_to_pfdl, dashboard_host_address=dashboard).dispatcher_object,
                         log_info=service_tracking,
                         device_registry_url=device_registry_url,
                         docker=docker,
                         number_default_clients=number_default_clients
                         ).main())

