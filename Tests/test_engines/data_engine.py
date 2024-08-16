from execution_engine_logic.data_object.declare_pfdl_structs import ExtractPFDL
from Tests.test_callbacks.data_callback import DispatcherTestCallbackFunctions
from Dispatcher.dispatcher_callbacks.provide_parametert_to_the_scheduler import provide_struct_parameter
import time
import unittest
class DataEngine(unittest.TestCase):

    def main(self, dispatcher_object):
        self.dispatcher = dispatcher_object
        process_pfdl = ExtractPFDL()
        #test structs
        struct_dict = process_pfdl.create_struct_dict(self.dispatcher.structs)
        self.check_created_struct_dict(struct_dict)
        callbacks = DispatcherTestCallbackFunctions(None, None, process_pfdl, self)
        self.dispatcher.set_callbacks(callbacks)
        self.dispatcher.register_dispatcher_callbacks(provide_struct_parameter(self.dispatcher, None, None).provide_parameter)
        self.dispatcher.run_dispatcher()
        while self.dispatcher.running:
            time.sleep(0.1)

    def check_created_struct_dict(self, struct_dict):
        Test_Structures = {'Struct': ['SWAP_Order', 'Stand_Segment', 'Light_Segment', 'Raw_Material', 'Blank'],
                           'Variable_Name': [['order_id', 'stand', 'segments', 'number_light_segments'], ['stand_shape', 'stand_height', 'stand_id', 'mat'], ['color', 'diameter', 'segment_id'], ['blanks', 'blank_number'], ['blank_type', 'blank_id', 'part_id']],
                           'Variable_Type': [['Double', 'Struct', 'Struct', 'Double'], ['String', 'Double', 'String', 'Struct'], ['String', 'Double', 'String'], ['Struct', 'Double'], ['String', 'String', 'Double']],
                           'Array_Length': [[None, 'None', 'Unspecific', None], [None, None, None, 'Unspecific'], [None, None, None], ['Unspecific', None], [None, None, None]],
                           'Referred_Struct': [[None, 'Stand_Segment', 'Light_Segment', None], [None, None, None, 'Raw_Material'], [None, None, None], ['Blank', None], [None, None, None]]}

        for i in range(len(struct_dict['Struct'])):
            self.assertEqual(struct_dict['Struct'][i], Test_Structures['Struct'][i])
            for j in range(len(struct_dict['Variable_Name'][i])):
                self.assertEqual(struct_dict['Variable_Name'][i][j], Test_Structures['Variable_Name'][i][j])
                self.assertEqual(struct_dict['Variable_Type'][i][j], Test_Structures['Variable_Type'][i][j])
                self.assertEqual(struct_dict['Array_Length'][i][j], Test_Structures['Array_Length'][i][j])
                self.assertEqual(struct_dict['Referred_Struct'][i][j], Test_Structures['Referred_Struct'][i][j])





