'''
Created by auto_sdk on 2019.08.05
'''
from dingtalk.api.base import RestApi
class OapiWorkspaceProjectMemberRoleUpdateRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.member_role = None
		self.project_id = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.workspace.project.member.role.update'
