from message.downstream.BaseMqttCommand import BaseMqttCommand
from core.internals.constants.ArrivedTopicPattern import ArrivedTopicPattern
from message.upstream.ota.Firmware import Firmware
import re


class OtaUpgradeCommand(BaseMqttCommand):

   def getMatchTopicPattern(self):
       return re.compile(ArrivedTopicPattern.DEVICE_OTA_COMMAND)

   def decodeToObject(self, msg):
       base = OtaUpgradeCommand()
       base.__dict__ = msg
       return base

   def getClass(self):
       return 'OtaUpgradeCommand'

   def getFirmwareInfo(self):
       firmware = Firmware()
       map = self.params
       firmware.version = map.get('version')
       firmware.signMethod = map.get('signMethod')
       firmware.sign = map.get('sign')
       firmware.fileUrl = map.get('fileUrl')
       firmware.fileSize = map.get('fileSize')
       return firmware
