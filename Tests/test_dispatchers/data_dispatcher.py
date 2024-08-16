from pfdl_scheduler.api.service_api import ServiceAPI
from pfdl_scheduler.scheduler import Scheduler, Event
from pfdl_scheduler.api.task_api import TaskAPI
from Tests.test_callbacks.data_callback import DispatcherTestCallbackFunctions
from Types.internal_data_converter import PFDL_EE_DataConverter
from Types.types import EE_Array, EE_Struct
import unittest
from pfdl_scheduler.model.struct import Struct
from pfdl_scheduler.model.array import Array

class dispatcher(unittest.TestCase):

    def __init__(self, dashboard: [str, None], path_to_pfdl: str):
        super().__init__()
        self.dispatcher = Scheduler(path_to_pfdl, dashboard_host_address = dashboard) if dashboard else Scheduler(path_to_pfdl)
        self.structs = self.dispatcher.process.structs
        self.dispatcher_callbacks = None
        self.converter = PFDL_EE_DataConverter()

    def set_callbacks(self, callbacks: DispatcherTestCallbackFunctions):
        self.dispatcher_callbacks = callbacks

    def register_dispatcher_callbacks(self, provide_parameter):
        self.dispatcher.register_callback_service_started(self.service_started_callback_wrapper)
        self.dispatcher.register_callback_service_finished(self.service_finished_callback_wrapper)
        self.dispatcher.register_callback_task_started(self.task_started_callback_wrapper)
        self.dispatcher.register_callback_task_finished(self.task_finished_callback_wrapper)
        self.dispatcher.register_variable_access_function(provide_parameter)

    def run_dispatcher(self):
        self.dispatcher.start()

    def fire_dispatcher_event(self, service_uuid):
        self.dispatcher.fire_event(Event(event_type="service_finished",
                      data={"service_id": service_uuid}))
    def running(self):
        return self.dispatcher.running

    def task_finished_callback_wrapper(self, task_api: TaskAPI):
        task_context_uuid = task_api.uuid if task_api.task.name == "productionTask" else task_api.task_context.uuid
        self.dispatcher_callbacks.task_finished_cb(task_api.task.name, task_api.uuid, task_context_uuid, task_api.task.output_parameters)

    def task_started_callback_wrapper(self, task_api: TaskAPI):
        task_context_uuid = task_api.uuid if task_api.task.name == "productionTask" else task_api.task_context.uuid
        input_parameters = []
        if len(task_api.input_parameters) > 0:
            for i in range(len(task_api.input_parameters)):
                if isinstance(task_api.input_parameters[i], Struct):
                    input_parameters.append(self.converter.create_ee_format(task_api.input_parameters[i]))
                else:
                    input_parameters.append(task_api.input_parameters[i])
        if task_api.task.name != "productionTask":
            self.check_data_converter(input_parameters)
        self.dispatcher_callbacks.task_started_cb(task_api.task.name, task_api.uuid, task_context_uuid, task_api.task.input_parameters, input_parameters, False, self)


    def service_finished_callback_wrapper(self, service_api: ServiceAPI):
        self.dispatcher_callbacks.service_finished_cb(service_api.service.name, service_api.task_context.uuid, service_api.uuid)

    def service_started_callback_wrapper(self, service_api: ServiceAPI):
        self.dispatcher_callbacks.service_started_cb(service_api.service.name, service_api.uuid, service_api.task_context.uuid, service_api.input_parameters , service_api.service.output_parameters)


    def check_data_converter(self, input_parameter):
        blank_1 = EE_Struct("Blank")
        blank_1.data_type = 'Blank'
        blank_1.add_attribute('blank_id', 'test1')
        blank_1.add_attribute('blank_type', 'test1')
        blank_1.add_attribute('part_id', 5)

        blank_2 = EE_Struct("Blank")
        blank_2.data_type = 'Blank'
        blank_2.add_attribute('blank_id', 'test2')
        blank_2.add_attribute('blank_type', 'test2')
        blank_2.add_attribute('part_id', 6)

        blanks_1 = EE_Array('blanks', 2)
        blanks_1.set_array_type('Blank')
        blanks_1.values = [blank_1, blank_2]

        blank_3 = EE_Struct("Blank")
        blank_3.data_type = 'Blank'
        blank_3.add_attribute('blank_id', 'test3')
        blank_3.add_attribute('blank_type', 'test3')
        blank_3.add_attribute('part_id', 7)

        blank_4 = EE_Struct("Blank")
        blank_4.data_type = 'Blank'
        blank_4.add_attribute('blank_id', 'test4')
        blank_4.add_attribute('blank_type', 'test4')
        blank_4.add_attribute('part_id', 8)

        blanks_2 = EE_Array('blanks', 2)
        blanks_2.set_array_type('Blank')
        blanks_2.values = [blank_3, blank_4]

        blanks_1_struct = EE_Struct("Raw_Material")
        blanks_1_struct.set_struct_type("Raw_Material")
        blanks_1_struct.add_attribute('blank_number', 2)
        blanks_1_struct.add_attribute('blanks', blanks_1)

        blanks_2_struct = EE_Struct("Raw_Material")
        blanks_2_struct.set_struct_type("Raw_Material")
        blanks_2_struct.add_attribute('blank_number', 2)
        blanks_2_struct.add_attribute('blanks', blanks_2)

        mat = EE_Array("mat", 2)
        mat.set_array_type("Raw_Material")
        mat.values = [blanks_1_struct, blanks_2_struct]

        stand = EE_Struct("stand")
        stand.set_struct_type('Stand_Segment')
        stand.add_attribute('mat', mat)
        stand.add_attribute('stand_height', 3)
        stand.add_attribute('stand_id', "Default")
        stand.add_attribute('stand_shape', 'plate')

        seg_1 = EE_Struct('Light_Segment')
        seg_1.set_struct_type('Light_Segment')
        seg_1.add_attribute('color', "red")
        seg_1.add_attribute('diameter', 5)
        seg_1.add_attribute('segment_id', "Default")

        seg_2 = EE_Struct('Light_Segment')
        seg_2.set_struct_type('Light_Segment')
        seg_2.add_attribute('color', "green")
        seg_2.add_attribute('diameter', 5)
        seg_2.add_attribute('segment_id', "Default")

        segments = EE_Array('segments', 2)
        segments.set_array_type("Light_Segment")
        segments.values = [seg_1, seg_2]

        SWAP_Order = EE_Struct("SWAP_Order")
        SWAP_Order.set_struct_type("SWAP_Order")
        SWAP_Order.add_attribute('order_id', 1000)
        SWAP_Order.add_attribute('stand', stand)
        SWAP_Order.add_attribute('segments', segments)
        SWAP_Order.add_attribute('number_light_segments', 5)

        self.assertEqual(input_parameter[0].attributes['order_id'], SWAP_Order.attributes['order_id'])
        self.assertEqual(input_parameter[0].data_type, SWAP_Order.data_type)
        self.assertEqual(input_parameter[0].name, SWAP_Order.name)
        self.assertEqual(input_parameter[0].attributes['number_light_segments'], SWAP_Order.attributes['number_light_segments'])


        self.assertEqual(input_parameter[0].attributes['segments'].data_type, SWAP_Order.attributes['segments'].data_type)
        self.assertEqual(input_parameter[0].attributes['segments'].length, SWAP_Order.attributes['segments'].length)
        self.assertEqual(input_parameter[0].attributes['segments'].name, SWAP_Order.attributes['segments'].name)

        self.assertEqual(input_parameter[0].attributes['segments'].values[0].data_type, SWAP_Order.attributes['segments'].values[0].data_type)
        self.assertEqual(input_parameter[0].attributes['segments'].values[0].name, SWAP_Order.attributes['segments'].values[0].name)
        self.assertEqual(input_parameter[0].attributes['segments'].values[0].attributes['color'], SWAP_Order.attributes['segments'].values[0].attributes['color'])
        self.assertEqual(input_parameter[0].attributes['segments'].values[0].attributes['diameter'], SWAP_Order.attributes['segments'].values[0].attributes['diameter'])
        self.assertEqual(input_parameter[0].attributes['segments'].values[0].attributes['segment_id'], SWAP_Order.attributes['segments'].values[0].attributes['segment_id'])

        self.assertEqual(input_parameter[0].attributes['segments'].values[1].data_type, SWAP_Order.attributes['segments'].values[1].data_type)
        self.assertEqual(input_parameter[0].attributes['segments'].values[1].name, SWAP_Order.attributes['segments'].values[1].name)
        self.assertEqual(input_parameter[0].attributes['segments'].values[1].attributes['color'], SWAP_Order.attributes['segments'].values[1].attributes['color'])
        self.assertEqual(input_parameter[0].attributes['segments'].values[1].attributes['diameter'], SWAP_Order.attributes['segments'].values[1].attributes['diameter'])
        self.assertEqual(input_parameter[0].attributes['segments'].values[1].attributes['segment_id'], SWAP_Order.attributes['segments'].values[1].attributes['segment_id'])

        self.assertEqual(input_parameter[0].attributes['stand'].data_type, SWAP_Order.attributes['stand'].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].name, SWAP_Order.attributes['stand'].name)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['stand_height'], SWAP_Order.attributes['stand'].attributes['stand_height'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['stand_id'], SWAP_Order.attributes['stand'].attributes['stand_id'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['stand_shape'], SWAP_Order.attributes['stand'].attributes['stand_shape'])

        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].data_type, SWAP_Order.attributes['stand'].attributes['mat'].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].name, SWAP_Order.attributes['stand'].attributes['mat'].name)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].length, SWAP_Order.attributes['stand'].attributes['mat'].length)

        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].data_type, SWAP_Order.attributes['stand'].attributes['mat'].values[0].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].name, SWAP_Order.attributes['stand'].attributes['mat'].values[0].name)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blank_number'], SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blank_number'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].data_type, SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].length, SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].length)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].name, SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].name)

        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].data_type, SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].name, SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].name)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].attributes['blank_id'], SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].attributes['blank_id'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].attributes['blank_type'], SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].attributes['blank_type'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].attributes['part_id'], SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[0].attributes['part_id'])

        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].data_type, SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].name, SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].name)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].attributes['blank_id'], SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].attributes['blank_id'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].attributes['blank_type'], SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].attributes['blank_type'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].attributes['part_id'], SWAP_Order.attributes['stand'].attributes['mat'].values[0].attributes['blanks'].values[1].attributes['part_id'])


        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].data_type, SWAP_Order.attributes['stand'].attributes['mat'].values[1].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].name, SWAP_Order.attributes['stand'].attributes['mat'].values[1].name)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blank_number'], SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blank_number'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].data_type, SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].length, SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].length)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].name, SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].name)

        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].data_type, SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].name, SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].name)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].attributes['blank_id'], SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].attributes['blank_id'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].attributes['blank_type'], SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].attributes['blank_type'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].attributes['part_id'], SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[0].attributes['part_id'])

        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].data_type, SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].data_type)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].name, SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].name)
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].attributes['blank_id'], SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].attributes['blank_id'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].attributes['blank_type'], SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].attributes['blank_type'])
        self.assertEqual(input_parameter[0].attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].attributes['part_id'], SWAP_Order.attributes['stand'].attributes['mat'].values[1].attributes['blanks'].values[1].attributes['part_id'])









