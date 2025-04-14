# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2025 (c) Fraunhofer IOSB (Author: Florian Düwel)
import asyncio
from external_modules.order_prioritizer.server.run_prioritizer_instance import PrioritizerServer

if __name__ == "__main__":
    asyncio.run(PrioritizerServer("opc.tcp://localhost:", "12000", "opc.tcp://localhost:8000", "opc.tcp://localhost:", 5).run_server())
