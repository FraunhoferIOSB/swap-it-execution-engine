# Execution Engine

## Installation Requirements

**Execution Engine:**

- asyncua==0.9.98
- nest-asyncio

**PFDL Scheduler:**

- antlr4-python3-runtime==4.9.3

- antlr-denter

- snakes

- install Graphviz:

  - **Important Note**: on Windows OS it is not possible to install Graphviz with pip. It has to be downloaded and installed manually. The download packages can be found here:

  -  https://graphviz.org/download/




After cloning the git, the submodule pfdl_scheduler has to be updated with: 

- git submodule update --init --recursive

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