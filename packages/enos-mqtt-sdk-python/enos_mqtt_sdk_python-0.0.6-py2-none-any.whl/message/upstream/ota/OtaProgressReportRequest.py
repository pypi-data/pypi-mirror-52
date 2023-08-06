from message.upstream.BaseMqttRequest import BaseMqttRequest
from message.upstream.BaseMqttRequest import Builder
from core.internals.constants.MethodConstants import MethodConstants
from core.internals.constants.DeliveryTopicFormat import DeliveryTopicFormat
from message.upstream.ota.OtaProgressReportResponse import OtaProgressReportResponse


class OtaProgressReportRequest(BaseMqttRequest):

    @classmethod
    def builder(cls):
        return Builder()

    def check(self):
        super(OtaProgressReportRequest, self).check()

    def _getPK_DK_FormatTopic(self):
        return DeliveryTopicFormat.PROGRESS_REPORT_TOPIC_FMT

    def getAnswerType(self):
        return OtaProgressReportResponse()

    def getResponse(self):
        return OtaProgressReportResponse()



class Builder(Builder):

    def __init__(self):
        super(Builder, self).__init__()
        self.params = dict(step='', desc='')

    def setStep(self, step):
        self.params['step'] = step
        return self

    def setDesc(self, desc):
        self.params['desc'] = desc
        return self

    def createMethod(self):
        return MethodConstants.OTA_PROGRESS

    def createParams(self):
        return self.params

    def createRequestInstance(self):
        return OtaProgressReportRequest()