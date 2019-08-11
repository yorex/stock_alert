'''
Created by auto_sdk on 2019.07.22
'''
from dingtalk.api.base import RestApi
class OapiAttendanceGroupPositionsRemoveRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.group_key = None
		self.op_userid = None
		self.wifi_key_list = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.attendance.group.positions.remove'
