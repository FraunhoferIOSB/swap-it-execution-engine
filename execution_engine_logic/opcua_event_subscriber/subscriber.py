import asyncio
from asyncua import Client
import json, threading, time
import paho.mqtt.client as mqtt

class MQTTClient:

    def __init__(self, broker="localhost", port=1884, topic="opcua/events"):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.connect()

    def connect(self):
        self.client.connect(self.broker, int(self.port))
        print(f"Connected to MQTT Broker at {self.broker}:{self.port}")

    def publish(self, message):
        self.client.publish(self.topic, json.dumps(message))

class SubHandlerStarted:

    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def event_notification(self, event):
        custom_properties = {}
        for (i, j) in event.get_event_props_as_fields_dict().items():
            if (str(i) == "service_uuid" or
                    str(i) == "service_name" or
                    str(i) == "time" or
                    str(i) == "ee_url"):
                custom_properties[i] = j.Value
        self.mqtt_client.publish(custom_properties)

class SubHandlerTaskStarted:

    def event_notification(self, event):
        custom_properties = {}
        for (i, j) in event.get_event_props_as_fields_dict().items():
            if (str(i) == "service_uuid" or
                    str(i) == "service_name" or
                    str(i) == "time" or
                    str(i) == "ee_url"):
                custom_properties[i] = j.Value

class SubHandlerTaskFinished:

    def event_notification(self, event):
        custom_properties = {}
        for (i,j) in event.get_event_props_as_fields_dict().items():
            if (str(i) == "service_uuid" or
                    str(i) == "service_name" or
                        str(i) == "time" or
                            str(i) == "ee_url"):
                custom_properties[i] = j.Value

class SubHandlerFinished:

    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def event_notification(self, event):
        custom_properties = {}
        for (i,j) in event.get_event_props_as_fields_dict().items():
            if (str(i) == "service_uuid" or
                    str(i) == "service_name" or
                        str(i) == "time" or
                            str(i) == "ee_url"):
                custom_properties[i] = j.Value
        self.mqtt_client.publish(custom_properties)


class EventListener:

    def __init__(self, ee_url, dispatcher, mqtt_url, mqtt_port):
        self.client = None
        self.server_object = None
        self.ee_url = ee_url
        self.dispatcher = dispatcher
        self.mqtt_url =  mqtt_url
        self.mqtt_port = mqtt_port
        self.mqtt_client = MQTTClient(broker=self.mqtt_url, port=self.mqtt_port) if ((self.mqtt_port is not None) or (self.mqtt_url is not None)) else MQTTClient()

    async def subscribe_service_started(self):
        myevent = await self.client.nodes.root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "3:ServiceStartedEvent"])
        sub = await self.client.create_subscription(100, SubHandlerStarted(self.mqtt_client))
        await sub.subscribe_events(self.server_object, myevent)

    async def subscribe_service_finished(self):
        myevent = await self.client.nodes.root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "3:ServiceFinishedEvent"])
        sub = await self.client.create_subscription(100,SubHandlerFinished(self.mqtt_client))
        await sub.subscribe_events(self.server_object, myevent)

    async def subscribe_task_started(self):
        myevent = await self.client.nodes.root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "3:TaskFinishedEvent"])
        sub = await self.client.create_subscription(100, SubHandlerTaskStarted())
        await sub.subscribe_events(self.server_object, myevent)

    async def subscribe_task_finished(self):
        myevent = await self.client.nodes.root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "3:TaskStartedEvent"])
        sub = await self.client.create_subscription(100,SubHandlerTaskFinished())
        await sub.subscribe_events(self.server_object, myevent)

    async def main(self):
        async with Client(url=self.ee_url) as self.client:
            self.server_object = self.client.get_node("ns=0;i=2253")
            await self.subscribe_service_started()
            await self.subscribe_service_finished()
            await self.subscribe_task_started()
            await self.subscribe_task_finished()
            while self.dispatcher.run_dispatcher():
                await asyncio.sleep(1)

    def start_client(self):
        control_interface_loop = asyncio.new_event_loop()
        control_interface_loop.run_until_complete(self.main())

    def run(self):
        thread = threading.Thread(target=self.start_client)
        thread.start()

