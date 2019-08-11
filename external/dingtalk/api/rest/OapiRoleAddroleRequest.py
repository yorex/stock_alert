'''
Created by auto_sdk on 2018.07.25
'''
from dingtalk.api.base import RestApi
class OapiRoleAddroleRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.groupId = None
		self.roleName = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.role.addrole'
