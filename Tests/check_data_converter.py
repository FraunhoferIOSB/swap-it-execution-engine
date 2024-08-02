import unittest
from Tests.test_engines.data_engine import DataEngine
from Tests.test_dispatchers.data_dispatcher import dispatcher


class check_type_converter(unittest.TestCase):

    def test_check_types(self):
        dispatcher_object = dispatcher(None, "./pfdl_files/data_converter.pfdl")
        DataEngine().main(dispatcher_object)




if __name__ == "__main__":
    unittest.main()