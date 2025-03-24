# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from asyncua import ua
from external_modules.order_prioritizer.server.method_callbacks import Callbacks

class Namespace:

    def __init__(self, server):
        self.server = server
        self.idx = 2
        self.name = "PriorityObject"
        self.variable_node = None
        self.priority_object = None

    async def add_namespace(self):
        #add a prioritizing object with a variable for all current orders and their priority value, a method to add orders and a method to remove orders
        self.priority_object = await self.server.nodes.objects.add_object(self.idx, self.name)
        self.variable_node = await self.priority_object.add_variable(self.idx, "OrderList", [], ua.VariantType.String)
        await self.variable_node.set_writable()
        cb = Callbacks(self.server, self.variable_node)
        method_1 = await self.priority_object.add_method(f"ns={self.idx};s=add_order", "2:add_order", cb.add_order, [ua.VariantType.String, ua.VariantType.String], [ua.VariantType.String])
        children = await method_1.get_children()
        for child in children:
            bn = await child.read_browse_name()
            if str(bn.Name) == "InputArguments":
                val = await child.read_value()
                val[0].Name = "orderId"
                val[1].Name = "priority"
                await child.write_value(val)
            elif str(bn.Name) == "OutputArguments":
                val = await child.read_value()
                val[0].Name = "result"
                await child.write_value(val)
        method_2 = await self.priority_object.add_method(f"ns={self.idx};s=remove_order", "2:remove_order", cb.remove_order, [ua.VariantType.String], [ua.VariantType.String])
        children = await method_2.get_children()
        for child in children:
            bn = await child.read_browse_name()
            if str(bn.Name) == "InputArguments":
                val = await child.read_value()
                val[0].Name = "orderId"
                await child.write_value(val)
            elif str(bn.Name) == "OutputArguments":
                val = await child.read_value()
                val[0].Name = "result"
                await child.write_value(val)


