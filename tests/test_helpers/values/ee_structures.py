from execution_engine_logic.data_types.types import EngineArray, EngineStruct

class DemoScenarioStructureTypes:

    def __init__(self):
        self.swap_order = None
        self.light_segment = None
        self.stand_segment = None
        self.raw_material = None
        self.blank = None
        self.create_type_descriptions()

    def create_type_descriptions(self):
        self.blank = EngineStruct("Blank")
        self.blank.set_struct_type("Blank")
        self.blank.add_attribute("blank_type", "string")
        self.blank.add_attribute("blank_id", "string")
        self.blank.add_attribute("part_id", "number")

        self.raw_material = EngineStruct("Raw_Material")
        self.raw_material.set_struct_type("Raw_Material")
        blank_array = EngineArray("blanks", 2)
        blank_array.data_type = "Blank"
        blank_array.values = []
        self.raw_material.add_attribute("blanks", blank_array)
        self.raw_material.add_attribute("blank_number", "number")

        self.light_segment = EngineStruct("Light_Segment")
        self.light_segment.set_struct_type("Light_Segment")
        self.light_segment.add_attribute("color", "string")
        self.light_segment.add_attribute("diameter", "number")
        self.light_segment.add_attribute("segment_id", "string")

        self.stand_segment = EngineStruct("Stand_Segment")
        self.stand_segment.set_struct_type("Stand_Segment")
        self.stand_segment.add_attribute("stand_shape", "string")
        self.stand_segment.add_attribute("stand_height", "number")
        self.stand_segment.add_attribute("stand_id", "string")

        self.swap_order = EngineStruct("SWAP_Order")
        self.swap_order.set_struct_type("SWAP_Order")
        self.swap_order.add_attribute("order_id", "number")
        self.swap_order.add_attribute("stand", "Stand_Segment")
        segments = EngineArray("segments", -1)
        segments.set_array_type("Light_Segment")
        segments.add_value([])
        self.swap_order.add_attribute("segments", segments)
        self.swap_order.add_attribute("number_light_segments", "number")


class DemoScenarioStructureValues:

    def __init__(self):
        self.swap_order = None
        self.light_segment = None
        self.stand_segment = None
        self.raw_material = None
        self.blank = None
        self.create_type_values()

    def create_type_values(self):
        self.blank = EngineStruct("Blank")
        self.blank.set_struct_type("Blank")
        self.blank.add_attribute("blank_type", "test")
        self.blank.add_attribute("blank_id", "test")
        self.blank.add_attribute("part_id", 123)

        self.light_segment = EngineStruct("Light_Segment")
        self.light_segment.set_struct_type("Light_Segment")
        self.light_segment.add_attribute("color", "red")
        self.light_segment.add_attribute("diameter", 5)
        self.light_segment.add_attribute("segment_id", "Default")

        self.stand_segment = EngineStruct("Stand_Segment")
        self.stand_segment.set_struct_type("Stand_Segment")
        self.stand_segment.add_attribute("stand_shape", "plate")
        self.stand_segment.add_attribute("stand_height", 3)
        self.stand_segment.add_attribute("stand_id", "Default")

        self.raw_material = EngineStruct("Raw_Material")
        self.raw_material.set_struct_type("Raw_Material")
        blank_array = EngineArray("blanks", 2)

        blank_1 = EngineStruct("Blank")
        blank_1.set_struct_type("Blank")
        blank_1.add_attribute("blank_type", "test")
        blank_1.add_attribute("blank_id", "test")
        blank_1.add_attribute("part_id", 123)

        blank_2 = EngineStruct("Blank")
        blank_2.set_struct_type("Blank")
        blank_2.add_attribute("blank_type", "test")
        blank_2.add_attribute("blank_id", "test")
        blank_2.add_attribute("part_id", 123)

        blank_array.data_type = "Blank"
        blank_array.values = [blank_1, blank_2]
        self.raw_material.add_attribute("blanks", blank_array)
        self.raw_material.add_attribute("blank_number", 2)

        self.swap_order = EngineStruct("SWAP_Order")
        self.swap_order.set_struct_type("SWAP_Order")
        self.swap_order.add_attribute("order_id", 1000)
        self.swap_order.add_attribute("stand", self.stand_segment)
        segments = EngineArray("segments", -1)
        segments.set_array_type("Light_Segment")
        light_segment = EngineStruct("Light_Segment")
        light_segment.set_struct_type("Light_Segment")
        light_segment.add_attribute("color", "green")
        light_segment.add_attribute("diameter", 5)
        light_segment.add_attribute("segment_id", "Default")
        segments.add_value(self.light_segment)
        segments.add_value(light_segment)
        self.swap_order.add_attribute("segments", segments)
        self.swap_order.add_attribute("number_light_segments", 5)



class DemoScenarioOPCUATypeInfo:
    def __init__(self):
        self.swap_order = []
        self.light_segment = []
        self.stand_segment = []
        self.raw_material = []
        self.blank = []
        self.create_type_descriptions()

    def create_type_descriptions(self):
        #blanks
        self.blank.append(FieldDescription("String", None, "blank_type"))
        self.blank.append(FieldDescription("String", None, "blank_id"))
        self.blank.append(FieldDescription("Double", None, "part_id"))
        #raw_material
        self.raw_material.append(FieldDescription("Blank", [1], "blanks"))
        self.raw_material.append(FieldDescription("Double", None, "blank_number"))
        #light_segment
        self.light_segment.append(FieldDescription("String", None, "color"))
        self.light_segment.append(FieldDescription("Double", None, "diameter"))
        self.light_segment.append(FieldDescription("String", None, "segment_id"))
        #stand_segment
        self.stand_segment.append(FieldDescription("String", None, "stand_shape"))
        self.stand_segment.append(FieldDescription("Double", None, "stand_height"))
        self.stand_segment.append(FieldDescription("String", None, "stand_id"))
        #swap_order
        self.swap_order.append(FieldDescription("String", None, "order_id"))
        self.swap_order.append(FieldDescription("Stand_Segment", None, "stand"))
        self.swap_order.append(FieldDescription("Light_Segment", [1], "segments"))
        self.swap_order.append(FieldDescription("Double", None, "number_light_segments"))

    def get_type_infor(self, req_type):
        if req_type == "SWAP_Order":
            return self.swap_order
        elif req_type == "Light_Segment":
            return self.light_segment
        elif req_type == "Stand_Segment":
            return self.stand_segment
        elif req_type == "Raw_Material":
            return self.raw_material
        elif req_type == "Blank":
            return self.blank
class FieldDescription:
    def __init__(self, dataType, arrayDim, name):
        self.dataType = dataType
        self.arrayDim = arrayDim
        self.name = name