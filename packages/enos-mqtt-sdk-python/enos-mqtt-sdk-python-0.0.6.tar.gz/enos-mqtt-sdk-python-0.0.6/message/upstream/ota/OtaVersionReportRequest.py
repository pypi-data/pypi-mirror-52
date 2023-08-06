from message.upstream.BaseMqttRequest import BaseMqttRequest
from message.upstream.BaseMqttRequest import Builder
from core.internals.constants.MethodConstants import MethodConstants
from core.internals.constants.DeliveryTopicFormat import DeliveryTopicFormat
from message.upstream.ota.OtaVersionReportResponse import OtaVersionReportResponse


class OtaVersionReportRequest(BaseMqttRequest):

    @classmethod
    def builder(cls):
        return Builder()

    def check(self):
        super(OtaVersionReportRequest, self).check()

    def _getPK_DK_FormatTopic(self):
        return DeliveryTopicFormat.VERSION_REPORT_TOPIC_FMT

    def getAnswerType(self):
        return OtaVersionReportResponse()

    def getResponse(self):
        return OtaVersionReportResponse()



class Builder(Builder):

    def __init__(self):
        super(Builder, self).__init__()
        self.params = dict(version='')

    def setVersion(self, version):
        self.params['version'] = version
        return self

    def createMethod(self):
        return MethodConstants.OTA_INFORM

    def createParams(self):
        return self.params

    def createRequestInstance(self):
        return OtaVersionReportRequest()