# Execution Engine

## Installation Requirements
```
  pip install asyncua==1.1.5 nest-asyncio==1.6.0 pfdl-scheduler==0.9.0
```
## Install

```
    pip install -r requirements.txt
```

## Python Version

```
    3.10.14
```

## Start the ExecutionEngine

To start the ExecutionEngine, it is required to adjust some parameters in the start_execution_engine.py file:
- path_to_pfdl **->** path to the directory where the PFDL file is stored
- execution_engine_server_url **->** url of the execution Engine
- iteration_time **->** iteration time of the execution engine
- Dashboard **->** activates the channel to the Dashboard
- service_tracking **->** provides log information about service/task started/finished events
  
## Build Documentation

To build the documentation, sphinx and the sphinx rtd theme are required. Both can be installed with:

    sphinx sphinx-rtd-theme myst_parser rst2pdf

Build the documentation:

    cd swap-it-demo-scenario
    #html
    sphinx-build -M html documentation/source/ documentation/build/html
    #pdf
    sphinx-build -b pdf documentation/source/ documentation/build/pdf/