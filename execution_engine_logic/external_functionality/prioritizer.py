from asyncua import Client
import asyncio, threading


class Prioritizer:

    def __init__(self, priority, proritizer_url, order_id, iteration_time, dispatcher):
        self.priority = priority
        self.proritizer_url = proritizer_url
        self.order_id = order_id
        self.iteration_time = iteration_time
        self.registered = False
        self.unregistered = False
        self.priority_object = None
        self.add_order = None
        self.remove_order = None
        self.client = None
        self.dispatcher = dispatcher

    async def browse_module(self):
        objects = self.client.nodes.objects
        objects_children = await objects.get_children()
        for child in objects_children:
            bn = await child.read_browse_name()
            if str(bn.Name) == "PriorityObject":
                self.priority_object = child
        for child in await self.priority_object.get_children():
            bn = await child.read_browse_name()
            if str(bn.Name) == "add_order":
                self.add_order = child
            if str(bn.Name) == "remove_order":
                self.remove_order = child

    async def register(self):
        await self.priority_object.call_method("2:add_order", *[self.order_id, self.priority])

    async def unregister(self):
        await self.priority_object.call_method("2:remove_order", self.order_id)

    def start(self):
        client_thread = threading.Thread(target=self.start_new_client_loop, daemon=True)
        client_thread.start()

    def start_new_client_loop(self):
        control_interface_loop = asyncio.new_event_loop()
        control_interface_loop.run_until_complete(self.run_client())

    async def run_client(self):
        while self.dispatcher.run_dispatcher():
            async with Client(self.proritizer_url) as self.client:
                await self.browse_module()
                run = True
                while run:
                    if self.registered == True:
                        await self.register()
                        self.registered = True
                        self.registered = False
                    if self.unregistered == True:
                        await self.unregister()
                        self.unregistered = False
                        run = False
                    await asyncio.sleep(self.iteration_time)
                await self.client.disconnect()

