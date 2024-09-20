# Execution Engine

## Start the ExecutionEngine

To start the ExecutionEngine, it is required to adjust some parameters in the start_execution_engine.py file:
- path_to_pfdl **->** path to the directory where the PFDL file is stored
- execution_engine_server_url **->** url of the execution Engine
- iteration_time **->** iteration time of the execution engine
- Dashboard **->** activates the channel to the Dashboard
- service_tracking **->** provides log information about service/task started/finished events

## OPC UA SDK Compatibility

Our approach is developed for the C-base open62541 OPC UA SDK (https://github.com/open62541/open62541). We also like to point to our swap-it-open62541-server template (https://github.com/FraunhoferIOSB/swap-it-open62541-server-template),
which provides a base c-library for a simple server configuration

On an experimental basis, the approach also works with python-asyncio (https://github.com/FreeOpcUa/opcua-asyncio).

## Installation Requirements
```
  pip install asyncua==1.1.5 nest-asyncio==1.6.0 pfdl-scheduler==0.9.0 coverage==7.6.1 python-on-whales==0.73.0
```
## Install

```
    pip install -r requirements.txt
```

## Python Version

```
    3.10.14
```

## Run Unit Tests with Coverage
    
    cd this repository
    coverage run --omit=tests/*,__init__.py tests/unit_tests/run_unit_tests.py

## Build Documentation

To build the documentation, sphinx and the sphinx rtd theme are required. Both can be installed with:

    sphinx sphinx-rtd-theme myst_parser rst2pdf

Build the documentation:

    cd this repository
    #html
    sphinx-build -M html documentation/source/ documentation/build/html
    #pdf
    sphinx-build -b pdf documentation/source/ documentation/build/pdf/