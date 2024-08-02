..
    Licensed under the MIT License.
    For details on the licensing terms, see the LICENSE file.
    SPDX-License-Identifier: MIT

    Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

.. _Execution Engine Logic:

===========================
Execution Engine Logic
===========================

The logic of the Execution Engine includes the OPC UA server of the Execution Engine, which in turn,
features the :ref:`Data Object` (1 in Figure). Since the DataObject provides all input and output parameter for processes,
corresponding OPC UA data types are required for the server (2 in Figure). Here, the Execution Engine provides an interface
to generate the corresponding types. This API is describe in :ref:`Generate OPC UA Types`.






.. figure:: /images/execution_engine_logic.png
   :alt: Overview
   :width: 100%


.. toctree::
   :maxdepth: 2

   DataObject
   GenerateOPCUATypes
   ServiceInterface