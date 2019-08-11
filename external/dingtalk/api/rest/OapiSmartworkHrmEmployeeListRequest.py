'''
Created by auto_sdk on 2019.07.01
'''
from dingtalk.api.base import RestApi
class OapiSmartworkHrmEmployeeListRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.field_filter_list = None
		self.userid_list = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.smartwork.hrm.employee.list'
