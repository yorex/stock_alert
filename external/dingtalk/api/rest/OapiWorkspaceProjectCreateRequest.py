'''
Created by auto_sdk on 2019.08.05
'''
from dingtalk.api.base import RestApi
class OapiWorkspaceProjectCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.open_project_create_dto = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.workspace.project.create'
