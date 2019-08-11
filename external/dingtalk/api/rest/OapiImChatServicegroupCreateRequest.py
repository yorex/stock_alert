'''
Created by auto_sdk on 2019.07.01
'''
from dingtalk.api.base import RestApi
class OapiImChatServicegroupCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.org_inner_group = None
		self.owner_userid = None
		self.title = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.im.chat.servicegroup.create'
