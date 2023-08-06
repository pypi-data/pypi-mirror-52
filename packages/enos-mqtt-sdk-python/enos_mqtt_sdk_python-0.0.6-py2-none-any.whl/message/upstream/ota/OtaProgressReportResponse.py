from message.upstream.BaseMqttResponse import BaseMqttResponse
from core.internals.constants.ArrivedTopicPattern import ArrivedTopicPattern
import re


class OtaProgressReportResponse(BaseMqttResponse):

   def getMatchTopicPattern(self):
       return re.compile(ArrivedTopicPattern.PROGRESS_REPORT_TOPIC_REPLY)

   def decodeToObject(self, msg):
       base = OtaProgressReportResponse()
       base.__dict__ = msg
       return base

   def getClass(self):
       return 'OtaProgressReportResponse'