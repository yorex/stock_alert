'''
Created by auto_sdk on 2019.07.26
'''
from dingtalk.api.base import RestApi
class OapiProcessFormGetRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.process_code = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.process.form.get'
