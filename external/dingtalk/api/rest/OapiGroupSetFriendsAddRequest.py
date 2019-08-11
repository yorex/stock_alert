'''
Created by auto_sdk on 2019.08.01
'''
from dingtalk.api.base import RestApi
class OapiGroupSetFriendsAddRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.chatid = None
		self.is_prohibit = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.group.set.friends.add'
