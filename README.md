# Execution Engine

## Start the ExecutionEngine

To start an Execution Engine for custom process execution, run the main.py file. However, the main Program requires a set of mandatory 
and optional arguments that must be handed over from as program arguments:

### Mandatory Arguments

- execution_engine_server_url 
- path_to_pfdl

Here, the execution_engine_server_url specifies the web-address of the Execution Engines OPC UA server and the 
path_to_pfdl a path to a local PFDL file that should be executed with the Execution Engine.

Example configurations could be:
- opc.tcp://localhost:4840
- ./PFDL_Examples/advanced.pdfl


### Optional Arguments
The optional arguments are used to create kwargs for the Execution Engine object. Here, each argument that is set must provide
a key and a value, separated by an equals. A potential configuration could be:

- "dashboard_host_address"="http://localhost:8080"
- "log_info"=True
- "device_registry_url"="opc.tcp://localhost:8000"
- "custom_url"="opc.tcp://localhost:"
- "number_default_clients"=5
- "assignment_agent_url"="opc.tcp://localhost:10000"
- "delay_start"=20"

### Run the main.py file

The main.py file can be started from a terminal with at least both mandatory program arguments set:

    python3 main.py "opc.tcp://localhost:4840" "./PFDL_Examples/advanced.pdfl"

In case that some or all optional arguments should be deployed, the command would look like:

    python3 main.py "opc.tcp://localhost:4840" "./PFDL_Examples/advanced.pdfl" "dashboard_host_address"="http://localhost:8080" "device_registry_url"="opc.tcp://localhost:8000" "number_default_clients"=5

## OPC UA SDK Compatibility

Our approach is developed for the C-base open62541 OPC UA SDK (https://github.com/open62541/open62541). We also like to point to our swap-it-open62541-server template (https://github.com/FraunhoferIOSB/swap-it-open62541-server-template),
which provides a base c-library for a simple server configuration

On an experimental basis, the approach also works with python-asyncio (https://github.com/FreeOpcUa/opcua-asyncio).

## Installation Requirements
```
  pip install asyncua==1.1.5 nest-asyncio==1.6.0 pfdl-scheduler==0.9.0 coverage==7.6.1 python-on-whales==0.73.0
```
Besides, Graphviz (https://graphviz.org/) must be installed on the system.
## Install

```
    pip install -r requirements.txt
```

## Python Version

```
    3.10.14
```

## Run Unit Tests 
    
    cd this repository
    python3 -m unittest tests/unit_tests/run_unit_tests.py 

## Run Unit Tests with Coverage
    
    cd this repository
    coverage run --omit=tests/*,__init__.py tests/unit_tests/run_unit_tests_with_coverage.py

## Build Documentation

To build the documentation, sphinx and the sphinx rtd theme are required. Both can be installed with:

    sphinx sphinx-rtd-theme myst_parser rst2pdf

Build the documentation:

    cd this repository
    #html
    sphinx-build -M html documentation/source/ documentation/build/html
    #pdf
    sphinx-build -b pdf documentation/source/ documentation/build/pdf/