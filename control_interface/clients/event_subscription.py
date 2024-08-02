# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)
from asyncua import ua
from datetime import datetime
import asyncio

class ServiceEvents:

    def __init__(self, client, server, handler, service_finished_event_type_node):
        self.client = client
        self.server = server
        self.handler = handler
        self.event = None
        self.service_finished_event_type_node = service_finished_event_type_node
        self.server_node = "ns=0;i=2253"

    async def get_custom_event_properties(self):
        browse_names, data_types = [], []
        for property in await self.event.get_properties():
            browse_names.append(await property.read_browse_name())
            data_types.append(await property.read_data_type())
        return browse_names, data_types

    async def create_select_clause(self, browse_names):
        select_clause = []
        for property in browse_names:
            Operand = ua.SimpleAttributeOperand()
            Operand.TypeDefinitionId = ua.NodeId(ua.ObjectIds.BaseEventType)
            Operand.BrowsePath = [property]
            Operand.AttributeId = ua.AttributeIds.Value
            select_clause.append(Operand)
        return select_clause

    async def set_where_clause(self):
        my_event_nodeId = await self.event.read_attribute(ua.AttributeIds.NodeId)
        where_clause = ua.ContentFilter([ua.ContentFilterElement(ua.FilterOperator.OfType,[ua.LiteralOperand(ua.Variant(my_event_nodeId.Value))])])
        return where_clause

    async def subscribe_event_with_filter(self, event_browse_name, client):
        custom_events = await client.get_node(self.service_finished_event_type_node).get_children()
        for child in custom_events:
            child_bn = await child.read_browse_name()
            if str(child_bn.Name) == str(event_browse_name):
                self.event = child
        browse_names, data_types = await self.get_custom_event_properties()
        subscription = await self.client.create_subscription(1, self.handler)
        if not browse_names:
            await subscription.subscribe_events(self.client.get_node(self.server_node), self.event)
        else:
            await subscription.subscribe_events(self.client.get_node(self.server_node), self.event,
                                                evfilter=ua.EventFilter(await self.create_select_clause(browse_names),
                                                                        WhereClause=await self.set_where_clause()))

    async def wait_event_results(self, handler):
        event_notification = False
        while event_notification == False:
            event_notification = handler.event_received
            await asyncio.sleep(self.server.iteration_time)
        return handler.event_results


class SubHandler():

    def __init__(self, client, tar_server, log_info):
        self.log_info = log_info
        self.event_results = []
        self.event_received = False
        self.client = client
        self.tar_server = tar_server

    async def event_notification(self, event):
        if self.log_info:
            print("[", datetime.now(), "] Client", self.client, "Received a new Service finished event from server:", self.tar_server, event)
        for (i,j) in event.get_event_props_as_fields_dict().items():
            self.event_results.append(j.Value)
        self.event_received = True