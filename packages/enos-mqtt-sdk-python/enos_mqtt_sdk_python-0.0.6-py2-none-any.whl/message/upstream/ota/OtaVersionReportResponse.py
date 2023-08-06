from message.upstream.BaseMqttResponse import BaseMqttResponse
from core.internals.constants.ArrivedTopicPattern import ArrivedTopicPattern
import re


class OtaVersionReportResponse(BaseMqttResponse):

   def getMatchTopicPattern(self):
       return re.compile(ArrivedTopicPattern.VERSION_REPORT_TOPIC_REPLY)

   def decodeToObject(self, msg):
       base = OtaVersionReportResponse()
       base.__dict__ = msg
       return base

   def getClass(self):
       return 'OtaVersionReportResponse'