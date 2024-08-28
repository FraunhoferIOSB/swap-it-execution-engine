from asyncua import ua
class ServiceParameter:
    def __init__(self, custom_types):
        self.light_segment = []
        self.stand = None
        self.swap_order = None
        self.custom_types = custom_types
        self.event_filter = None
        self.service_results = {"SyncReturn":[], "AsyncReturn":[]}
        self.set_values()
    def set_values(self):
        self.light_segment.append(self.get_custom_type("Light_Segment")(color=ua.String("red"), diameter=ua.Double(5.0), segment_id=ua.String("Default")))
        self.light_segment.append(self.get_custom_type("Light_Segment")(color=ua.String("green"), diameter=ua.Double(5.0), segment_id=ua.String("Default")))
        self.stand = self.get_custom_type("Stand_Segment")(stand_height=ua.Double(3.0), stand_id=ua.String("Default"), stand_shape=ua.String("plate"))
        self.swap_order = self.get_custom_type("SWAP_Order")(order_id=1000, number_light_segments=ua.Double(5.0), segments=self.light_segment, stand=self.stand)
        sao = ua.SimpleAttributeOperand(
            TypeDefinitionId=ua.NodeId(NodeIdType=ua.NodeIdType.FourByte, NamespaceIndex=0, Identifier=2041),
            BrowsePath=[ua.QualifiedName(NamespaceIndex=4, Name="order")],
            AttributeId=ua.AttributeIds.Value, IndexRange=None)
        content = ua.ContentFilter(Elements=[ua.ContentFilterElement(FilterOperator_=ua.FilterOperator.OfType,
                                                                     FilterOperands=[ua.LiteralOperand(
                                                                         Value=ua.Variant(
                                                                             Value=ua.NodeId(
                                                                                 NodeIdType=ua.NodeIdType.FourByte,
                                                                                 NamespaceIndex=4, Identifier=15001),
                                                                             VariantType=ua.VariantType.NodeId,
                                                                             Dimensions=None,
                                                                             is_array=False))])])
        self.event_filter = ua.EventFilter(SelectClauses=[sao], WhereClause=content)
        self.service_results["SyncReturn"].append(
            self.get_custom_type("ServiceExecutionAsyncResultDataType")(ServiceResultMessage='Message',
                                                                        ServiceResultCode=1,
                                                                        ExpectedServiceExecutionDuration=7.0,
                                                                        ServiceTriggerResult=self.get_custom_type("ServiceTriggerResult").SERVICE_RESULT_ACCEPTED))
        self.service_results["AsyncReturn"].append(self.swap_order)
    def get_custom_type(self, type):
        for name, obj in zip(self.custom_types["Name"], self.custom_types["Class"]):
            if(str(name) == str(type)):
                return obj