# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from asyncua import uamethod, ua

class Callbacks:

    def __init__(self, server, variable_node):
        self.variable_node = variable_node
        self.server = server

    @uamethod
    async def add_order(self, parent, order_id, priority):
        value = await self.variable_node.read_value()
        value.append([order_id, priority])
        await self.variable_node.write_value(ua.Variant(Value=value, VariantType=ua.VariantType.String, Dimensions=[len(value),2], is_array=True))
        return "order "+str(order_id)+ " added with Priority " + str(priority)

    @uamethod
    async def remove_order(self, parent, order_id):
        value = await self.variable_node.read_value()
        for val in value:
            if str(val[0]) == str(order_id):
                value.remove(val)
                break
        await self.variable_node.write_value(ua.Variant(value, ua.VariantType.String, Dimensions=[len(value),2],  is_array=True))
        return "order " + str(order_id) + " removed"

