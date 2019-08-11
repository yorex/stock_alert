'''
Created by auto_sdk on 2019.07.01
'''
from dingtalk.api.base import RestApi
class OapiCalendarDeleteRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.calendar_id = None
		self.userid = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.calendar.delete'
