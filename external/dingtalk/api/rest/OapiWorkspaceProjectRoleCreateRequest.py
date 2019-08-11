'''
Created by auto_sdk on 2019.08.05
'''
from dingtalk.api.base import RestApi
class OapiWorkspaceProjectRoleCreateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.open_tag_create_dto_list = None
		self.project_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.workspace.project.role.create'
