..
    Licensed under the MIT License.
    For details on the licensing terms, see the LICENSE file.
    SPDX-License-Identifier: MIT

    Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

.. _Getting Started:

================
Getting Started
================


.. _Configure an Execution Engine:

Configure an Execution Engine
=============================

To :ref:`simple started` with the :ref:`PFDL Scheduler` as dispatcher the main.py file must be executed.
Here, an instance of the Execution Engine class is created. Table 2 displays the mandatory and optional class arguments
for an Execution Engine. Optional class arguments have default values that can be overwritten by providing a corresponding
value when creating the Execution Engine object. A set of :ref:`Tutorials` is provided within this repository, where each of them features a different
:ref:`Resource Assignment` strategy of the Execution Engine.


As stated before, we integrate the :ref:`PFDL Scheduler` as default dispatcher for the Execution Engine. However,
if it is desired to replace the :ref:`PFDL Scheduler` as dispatcher and
integrate a custom dispatcher, have a look a section :ref:`Custom Dispatchers`. Anyway, the :ref:`PFDL Scheduler` must be set
as :ref:`Dispatcher Configuration`. Afterwards, an instance of the :ref:`PFDL Scheduler` must be handed
over to the Execution Engine object (Table 2). Table 1 displays the :ref:`Dispatcher Configuration` for the :ref:`PFDL Scheduler`



.. list-table:: **Table 1: Dispatcher Configuration**
   :widths: 50 50 50
   :header-rows: 1

   * - **Argument**
     - **Type**
     - **Explanation**
   * - filepath
     - str
     - | path to a file that contains the process description of the
       | process to be executed with the Execution Engine
   * - dashboard_host_address
     - str
     - | URL of a visualization tool for the process execution. For the
       | :ref:`PFDL Scheduler`, the `SWAP-IT Dashboard <https://github.com/iml130/swap-it-dashboard>`_ is provided.


.. _Execution Engine Class Argument:
.. list-table:: **Table 2: Execution Engine Class Arguments**
   :widths: 50 50 50
   :header-rows: 1

   * - **Argument**
     - **Type**
     - **Explanation**
   * - **Mandatory**
     -
     -
   * - server_url
     - str
     - Target URL of the Execution Engine's OPC UA server
   * - dispatcher_object
     - dispatcher
     - Python object of a configured dispatcher
   * - **Optional**
     -
     -
   * - iteration_time
     - float
     - | timespan between a loop operation of the Execution Engine's
       | OPC UA server. If no value is set, the iteration_time
       | defaults to iteration_time=0.001 seconds.
   * - log_info
     - bool
     - | The Execution Engine prints log messages about the
       | executed Tasks and Service. If no value is set, the
       | log_info defaults to log_info = False,
       | so that no log messages are printed.
   * - number_default_clients
     - int
     - | Number of OPC UA Clients that are started by the Execution
       | Engine's Control Interface. If no value is set, the value
       | defaults to number_default_clients = 1,
       | so that only a single client is started.
       | In case that more Clients are required e.g., due to parallel
       | service executions, the Execution Engine will start new
       | clients, however, this requires computational effort.
   * - device_registry_url
     - str
     - | URL of the Device Registry's OPC UA server. In case that no
       | value is set, it has to be ensured, that a static resource
       | assignment is provided (see :ref:`Resource Assignment`).
   * - assignment_agent_url
     - str
     - | URL of an Assignment Agent's OPC UA server. In case that
       | no value is set, either a static Assignment Agent must
       | be provided, or the default assignment behavior of the
       | Execution Engine is applied (see :ref:`Resource Assignment`).
   * - delay_start
     - int
     - | If set, the Execution Engine waits delay_start number
       | of seconds, otherwise, the process execution starts
       | without delay
   * - docker
     - string
     - | In case that the Execution Engine interacts with OPC UA
       | server inside a docker environment, it might be possible
       | that the server URL's have to be adjusted, so that the
       | Execution Engine can connect to them from outside the
       | docker environment. If set, the Port from the
       | server URL received from an Assignment Agent is extracted
       | and added to the string specified in this argument.
       | For example, if the Execution Engine receives an URL
       | "opc.tcp://swap_server:4840" docker = "opc.tcp://localhost:"
       | will adjust the url to "opc.tcp://localhost:4840".

.. _simple started:

Start an Execution Engine
==========================

An Execution Engine can simple be started with:

.. code-block:: python

    git clone https://github.com/FraunhoferIOSB/swap-it-execution-engine.git
    cd swap-it-execution-engine
    python main.py


**Important Note**
Ensure that the python version is greater 3.10 and the required python packages are installed:

.. code-block:: python

   pip install asyncua==1.1.5 nest-asyncio==1.6.0 pfdl-scheduler==0.9.0 coverage==7.6.1 python-on-whales==0.73.0




.. toctree::
   :maxdepth: 4

   Tutorials